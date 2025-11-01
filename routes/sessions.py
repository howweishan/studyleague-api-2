from flask import Blueprint, request, jsonify
from controllers import StudySessionController
from services.pocketbase_service import pocketbase_service
from schemas import StudySessionSchema
from marshmallow import ValidationError
from utils.auth import require_auth

# Use the global service instance
session_controller = StudySessionController(pocketbase_service)
session_schema = StudySessionSchema()

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/study_sessions')

@sessions_bp.route('/', methods=['GET'])
@require_auth
def get_sessions():
	"""Get study sessions with optional filtering"""
	try:
		user_id = request.args.get('user_id')
		active_only = request.args.get('active', 'false').lower() == 'true'
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 30, type=int)
		
		if user_id:
			if active_only:
				sessions = session_controller.get_active_sessions(user_id)
			else:
				sessions = session_controller.get_user_sessions(user_id)
		else:
			sessions = session_controller.get_all(page=page, per_page=per_page)
		
		return jsonify(sessions), 200
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<session_id>', methods=['GET'])
@require_auth
def get_session(session_id):
	"""Get session by ID"""
	try:
		session = session_controller.get_by_id(session_id, expand="user,room")
		if session:
			return jsonify(session), 200
		else:
			return jsonify({'error': 'Session not found'}), 404
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/', methods=['POST'])
@require_auth
def create_session():
	"""Create a new study session"""
	try:
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		# Validate data
		try:
			validated_data = session_schema.load(data)
		except ValidationError as e:
			return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
		
		if not isinstance(validated_data, dict):
			return jsonify({'error': 'Invalid payload format'}), 400
		
		session = session_controller.create(validated_data)
		if session:
			return jsonify(session), 201
		else:
			return jsonify({'error': 'Failed to create session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<session_id>', methods=['PUT'])
def update_session(session_id):
	"""Update study session"""
	try:
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		# Validate data (partial update)
		validated_data = session_schema.load(data, partial=True)
  
		if not isinstance(validated_data, dict):
			return jsonify({'error': 'Invalid payload format'}), 400
		
		session = session_controller.update(session_id, validated_data)
		if session:
			return jsonify(session), 200
		else:
			return jsonify({'error': 'Failed to update session'}), 500
	
	except ValidationError as e:
		return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<session_id>/end', methods=['POST'])
def end_session(session_id):
	"""End a study session"""
	try:
		session = session_controller.end_session(session_id)
		if session:
			return jsonify({'message': 'Session ended successfully', 'session': session}), 200
		else:
			return jsonify({'error': 'Failed to end session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
	"""Delete study session"""
	try:
		success = session_controller.delete(session_id)
		if success:
			return jsonify({'message': 'Session deleted successfully'}), 200
		else:
			return jsonify({'error': 'Failed to delete session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

# New endpoints for frontend session management

@sessions_bp.route('/start', methods=['POST'])
@require_auth
def start_session(user_id):
	"""Start a new study session"""
	try:
		data = request.get_json()
		timestamp = data.get('timestamp') if data else None
		
		# Create a new session for the user with active_duration starting at 1
		# (PocketBase requires min value of 1)
		session_data = {
			"user": user_id,
			"room": None,
			"active_duration": 0,
			"active": True,
			"integrity_score": None
		}
		session = session_controller.create(session_data)
		
		if session:
			return jsonify({
				'id': session.get('id'),
				'timestamp': timestamp
			}), 201
		else:
			return jsonify({'error': 'Failed to start session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/heartbeat', methods=['POST'])
@require_auth
def heartbeat(user_id):
	"""Receive heartbeat for active session and update duration"""
	try:
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		session_id = data.get('session_id')
		timestamp = data.get('timestamp')
		is_active = data.get('is_active', True)
		
		if not session_id:
			return jsonify({'error': 'session_id is required'}), 400
		
		# Get the current session
		session = session_controller.get_by_id(session_id)
		if not session:
			return jsonify({'error': 'Session not found'}), 404
		
		# Verify the session belongs to the authenticated user
		if session.get('user') != user_id:
			return jsonify({'error': 'Unauthorized access to session'}), 403
		
		# Get current active_duration
		current_duration = session.get('active_duration', 0)
		
		# Only increment duration if user is active
		if is_active:
			new_duration = current_duration + 1
		else:
			new_duration = current_duration
		
		# Update the session
		updated_session = session_controller.update(session_id, {
			'active_duration': new_duration,
			'active': is_active
		})
		
		if updated_session:
			return jsonify({
				'message': 'Heartbeat received',
				'duration': new_duration,
				'is_active': is_active
			}), 200
		else:
			return jsonify({'error': 'Failed to update session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@sessions_bp.route('/stop', methods=['POST'])
@require_auth
def stop_session(user_id):
	"""Stop a study session"""
	try:
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		session_id = data.get('session_id')
		timestamp = data.get('timestamp')
		
		if not session_id:
			return jsonify({'error': 'session_id is required'}), 400
		
		# Get the current session
		session = session_controller.get_by_id(session_id)
		if not session:
			return jsonify({'error': 'Session not found'}), 404
		
		# Verify the session belongs to the authenticated user
		if session.get('user') != user_id:
			return jsonify({'error': 'Unauthorized access to session'}), 403
		
		# End the session
		updated_session = session_controller.end_session(session_id)
		
		if updated_session:
			return jsonify({
				'message': 'Session stopped successfully',
				'session': updated_session
			}), 200
		else:
			return jsonify({'error': 'Failed to stop session'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500
