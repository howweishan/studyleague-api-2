from json import JSONDecodeError
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from controllers import UserController
from services.pocketbase_service import pocketbase_service
from schemas import UserSchema
from marshmallow import ValidationError

from utils.auth import require_auth
from utils.uri import cast_image_uri

# Use the global service instance
user_controller = UserController(pocketbase_service)
user_schema = UserSchema()

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/login', methods=['POST'])
def authenticate_user():
	"""Authenticate user and return PocketBase token"""
	try:
		data = request.get_json()
		
		# Ensure input present
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		# Ensure validated_data is properly structured
		validated_data = user_schema.load(data, partial=['username', 'passwordConfirm'])

		if not isinstance(validated_data, dict):
			return jsonify({'error': 'Invalid payload format'}), 400

		# Get from verified fields
		email = validated_data.get('email') or ""
		password = validated_data.get('password') or ""

		# Authenticate user
		auth_data = pocketbase_service.authenticate(email, password)

		# Process response
		if auth_data:
			if not auth_data['isValid']:
				print(auth_data['error'])
				return jsonify({'error': 'Invalid credentials'}), 401

			# Successful authentication
			return jsonify({
				'success': True,
				'token': auth_data['token'],
				'user': {
					'user_id': auth_data['user_id'],
					'username': auth_data['record'].get('username', ''),
					'first_name': auth_data['record'].get('first_name', ''),
					'last_name': auth_data['record'].get('last_name', ''),
					'dob': auth_data['record'].get('dob', None),
					'gender': auth_data['record'].get('gender', None),
					'role': auth_data['record'].get('role', 'user'),
					'isVerified': auth_data['record'].get('verified', False),
					'avatar_url': cast_image_uri(auth_data['record'].get('avatar', ''), 'users', auth_data['user_id']) if auth_data['record'].get('avatar') else None,
					'email': auth_data['record'].get('email', '')	
				}
			}), 200
		else:
			return jsonify({'error': 'Invalid credentials'}), 401
	except ValidationError as e:
		return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
	except BadRequest:
		return jsonify({'error': 'Invalid request format. Perhaps you made a mistake in comma?'}), 400
	except Exception as e:
		return jsonify({'error': str(e)}), 500
	
@users_bp.route('/logout', methods=['POST'])
@require_auth
def logout_user():
	"""Logout user (clear auth)"""
	try:
		pocketbase_service.clear_auth()
		return jsonify({
			'success': True,
			'message': 'Logged out successfully'
		}), 200

	except Exception as e:
		return jsonify({'error': str(e)}), 500

@users_bp.route('/user/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
	"""Get user by ID"""
	try:
		user = user_controller.get_user_profile(user_id)
		if user:
			return jsonify({
				'success': True,
				'avatar_url': cast_image_uri(user.get('avatar', ''), 'users', user_id) if user.get('avatar') else None,
				'dob': user.get('dob'),
				'email': user.get('email'),
				'username': user.get('username'),
				'first_name': user.get('first_name'),
				'last_name': user.get('last_name'),
				'role': user.get('role', 'user'),
				'isVerified': user.get('verified', False),
				'registered_at': user.get('created')
			}), 200
		else:
			return jsonify({'error': 'User not found'}), 404
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@users_bp.route('/', methods=['GET'])
@require_auth
def get_all_users():
	"""Get all users"""
	try:
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 30, type=int)
		
		users = user_controller.get_all(page=page, per_page=per_page)
		return jsonify({
			'success': True
		}), 200
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@users_bp.route('/signup', methods=['POST'])
def register_user():
	"""Create a new user"""
	try:
		data = request.get_json()
  
		# Sanitize data fields
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		# Validate data
		validated_data = user_schema.load(data)

		# Ensure validated_data is a dict before passing to controller
		if not isinstance(validated_data, dict):
			return jsonify({'error': 'Invalid payload format'}), 400

		# Create user
		user = user_controller.create(validated_data)
		if user:
			return jsonify({
				'success': True,
				"avatar_url": cast_image_uri(user.get('avatar', ''), 'users', user.user_id) if user.get('avatar') else None,
				'dob': user.get('dob'),
				'email': user.get('email'),
				'username': user.get('username'),
				'first_name': user.get('first_name'),
				'last_name': user.get('last_name'),
				'updated_at': user.get('updated')
			}), 201
		else:
			return jsonify({'error': 'Failed to create user'}), 500
	
	except ValidationError as e:
		return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
	 
	 
@users_bp.route('/user/<user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
	"""Update user details"""
	try:
		data = request.get_json()

		# Sanitize data fields
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		# Validate data (partial update)
		validated_data = user_schema.load(data, partial=['passwordConfirm', 'old_password', 'username', 'password', 'email'])
		# Ensure validated_data is a dict before passing to controller
		if not isinstance(validated_data, dict):
			return jsonify({'error': 'Invalid payload format'}), 400
		
		user = user_controller.update(user_id, validated_data)
		if user:
			return jsonify({
				'success': True,
				"avatar_url": cast_image_uri(user.get('avatar', ''), 'users', user_id) if user.get('avatar') else None,
				'dob': user.get('dob'),
				'email': user.get('email'),
				'username': user.get('username'),
				'first_name': user.get('first_name'),	
				'last_name': user.get('last_name'),
				'updated_at': user.get('updated')
			}), 200
		else:
			return jsonify({'error': 'Failed to update user'}), 500
	
	except ValidationError as e:
		return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
	"""Delete user"""
	try:
		success = user_controller.delete(user_id)
		if success:
			return jsonify({'message': 'User deleted successfully'}), 200
		else:
			return jsonify({'error': 'Failed to delete user'}), 500
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500
