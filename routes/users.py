from flask import Blueprint, request, jsonify
from controllers import UserController
from services.pocketbase_service import pocketbase_service
from schemas import UserSchema
from marshmallow import ValidationError

# Use the global service instance
user_controller = UserController(pocketbase_service)
user_schema = UserSchema()

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/auth', methods=['POST'])
def authenticate_user():
    """Authenticate user and return PocketBase token (like JavaScript version)"""
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Python equivalent of: const authData = await pb.collection("users").authWithPassword('test@example.com', '1234567890');
        auth_data = pocketbase_service.authenticate_user(data['email'], data['password'])
        
        if auth_data:
            # Return data similar to JavaScript version where you can access:
            # console.log(pb.authStore.isValid);
            # console.log(pb.authStore.token);
            # console.log(pb.authStore.record.id);
            if not auth_data['isValid']:
                print(auth_data['error'])
                return jsonify({'error': 'Invalid credentials'}), 401

            return jsonify({
                'success': True,
                'token': auth_data['token'],  # This is pb.authStore.token
                'user': auth_data['record'],  # This is pb.authStore.record
                'isValid': auth_data['isValid'],  # This is pb.authStore.isValid
                'user_id': auth_data['user_id'],  # This is pb.authStore.record.id
                'message': 'Authentication successful'
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/logout', methods=['POST'])
def logout_user():
    """Logout user (clear auth) - equivalent to pb.authStore.clear()"""
    try:
        # Get token from header to identify which session to clear
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            # In a real implementation, you might want to invalidate this specific token
            # For now, we'll just clear the current auth store
            pocketbase_service.clear_auth()
        
        return jsonify({'message': 'Logged out successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        # Check if request has valid token
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            pocketbase_service.set_auth_token(token)
        
        user = user_controller.get_user_profile(user_id)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        
        users = user_controller.get_all(page=page, per_page=per_page)
        return jsonify(users), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        validated_data = user_schema.load(data)
        
        user = user_controller.create(validated_data)
        if user:
            return jsonify(user), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data (partial update)
        validated_data = user_schema.load(data, partial=True)
        
        user = user_controller.update(user_id, validated_data)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
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
