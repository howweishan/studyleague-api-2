from flask import Blueprint, request, jsonify
from controllers import AchievementController, UserAchievementController
from services.pocketbase_service import pocketbase_service
from schemas import AchievementSchema, UserAchievementSchema
from marshmallow import ValidationError
from utils.auth import require_auth, get_auth_token_from_header

# Use the global service instance
achievement_controller = AchievementController(pocketbase_service)
user_achievement_controller = UserAchievementController(pocketbase_service)
achievement_schema = AchievementSchema()
user_achievement_schema = UserAchievementSchema()

achievements_bp = Blueprint('achievements', __name__, url_prefix='/api/achievements')

@achievements_bp.route('/', methods=['GET'])
@require_auth
def get_achievements():
    """Get all achievements"""
    try:
        achievements = achievement_controller.get_all_achievements()
        return jsonify(achievements), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/<achievement_id>', methods=['GET'])
def get_achievement(achievement_id):
    """Get achievement by ID"""
    try:
        achievement = achievement_controller.get_by_id(achievement_id)
        if achievement:
            return jsonify(achievement), 200
        else:
            return jsonify({'error': 'Achievement not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/user/<user_id>', methods=['GET'])
@require_auth
def get_user_achievements(user_id):
    """Get achievements for a specific user"""
    try:
        achievements = user_achievement_controller.get_user_achievements(user_id)
        return jsonify(achievements), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/unlock', methods=['POST'])
def unlock_achievement():
    """Unlock an achievement for a user"""
    try:
        data = request.get_json()
        if not data or 'user' not in data or 'achievement' not in data:
            return jsonify({'error': 'User and achievement IDs required'}), 400
        
        # Validate data
        validated_data = user_achievement_schema.load(data)
        
        user_achievement = user_achievement_controller.create(validated_data)
        if user_achievement:
            return jsonify(user_achievement), 201
        else:
            return jsonify({'error': 'Failed to unlock achievement'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/', methods=['POST'])
def create_achievement():
    """Create a new achievement (admin only)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        validated_data = achievement_schema.load(data)
        
        achievement = achievement_controller.create(validated_data)
        if achievement:
            return jsonify(achievement), 201
        else:
            return jsonify({'error': 'Failed to create achievement'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/<achievement_id>', methods=['PUT'])
def update_achievement(achievement_id):
    """Update achievement (admin only)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data (partial update)
        validated_data = achievement_schema.load(data, partial=True)
        
        achievement = achievement_controller.update(achievement_id, validated_data)
        if achievement:
            return jsonify(achievement), 200
        else:
            return jsonify({'error': 'Failed to update achievement'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@achievements_bp.route('/<achievement_id>', methods=['DELETE'])
def delete_achievement(achievement_id):
    """Delete achievement (admin only)"""
    try:
        success = achievement_controller.delete(achievement_id)
        if success:
            return jsonify({'message': 'Achievement deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete achievement'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
