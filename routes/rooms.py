from flask import Blueprint, request, jsonify
from controllers import StudyRoomController
from services.pocketbase_service import pocketbase_service
from schemas import StudyRoomSchema
from marshmallow import ValidationError

from utils.auth import require_auth

# Use the global service instance
room_controller = StudyRoomController(pocketbase_service)
room_schema = StudyRoomSchema()

rooms_bp = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@rooms_bp.route('/', methods=['GET'])
@require_auth
def get_rooms():
    """Get study rooms with optional filtering"""
    
    try:
        public_only = request.args.get('public', 'false').lower() == 'true'
        host_id = request.args.get('host_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        
        if public_only:
            rooms = room_controller.get_public_rooms()
        elif host_id:
            rooms = room_controller.get_user_rooms(host_id)
        else:
            rooms = room_controller.get_all(page=page, per_page=per_page, expand="host")
        
        return jsonify(rooms), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get room by ID"""
    try:
        room = room_controller.get_by_id(room_id, expand="host")
        if room:
            return jsonify(room), 200
        else:
            return jsonify({'error': 'Room not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/create', methods=['POST'])
def create_room():
    """Create a new study room"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        validated_data = room_schema.load(data)
        
        room = room_controller.create(validated_data)
        if room:
            return jsonify(room), 201
        else:
            return jsonify({'error': 'Failed to create room'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/<room_id>', methods=['PUT'])
def update_room(room_id):
    """Update study room"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data (partial update)
        validated_data = room_schema.load(data, partial=True)
        
        room = room_controller.update(room_id, validated_data)
        if room:
            return jsonify(room), 200
        else:
            return jsonify({'error': 'Failed to update room'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    """Delete study room"""
    try:
        success = room_controller.delete(room_id)
        if success:
            return jsonify({'message': 'Room deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete room'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
