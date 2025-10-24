from flask import Blueprint, request, jsonify
from controllers import DiscussionController, DiscussionReplyController
from schemas import DiscussionSchema, DiscussionReplySchema
from services.pocketbase_service import pocketbase_service
from marshmallow import ValidationError
from utils.auth import require_auth

# Schemas
discussion_schema = DiscussionSchema()
discussion_reply_schema = DiscussionReplySchema()

# Controllers
discussion_controller = DiscussionController(pocketbase_service)
discussion_reply_controller = DiscussionReplyController(pocketbase_service)


discussions_bp = Blueprint('discussions', __name__, url_prefix='/api/discussions')

@discussions_bp.route('/', methods=['GET'])
@require_auth
def get_discussions():
    """Get all discussions"""
    try:
        author_id = request.args.get('author_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        
        if author_id:
            discussions = discussion_controller.get_user_discussions(author_id)
        else:
            discussions = discussion_controller.get_all_discussions()
        
        return jsonify(discussions), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    """Get discussion by ID"""
    try:
        discussion = discussion_controller.get_by_id(discussion_id, expand="author")
        if discussion:
            return jsonify(discussion), 200
        else:
            return jsonify({'error': 'Discussion not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/', methods=['POST'])
def create_discussion():
    """Create a new discussion"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        validated_data = discussion_schema.load(data)
        
        discussion = discussion_controller.create(validated_data)
        if discussion:
            return jsonify(discussion), 201
        else:
            return jsonify({'error': 'Failed to create discussion'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<discussion_id>', methods=['PUT'])
def update_discussion(discussion_id):
    """Update discussion"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data (partial update)
        validated_data = discussion_schema.load(data, partial=True)
        
        discussion = discussion_controller.update(discussion_id, validated_data)
        if discussion:
            return jsonify(discussion), 200
        else:
            return jsonify({'error': 'Failed to update discussion'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<discussion_id>', methods=['DELETE'])
def delete_discussion(discussion_id):
    """Delete discussion"""
    try:
        success = discussion_controller.delete(discussion_id)
        if success:
            return jsonify({'message': 'Discussion deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete discussion'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Discussion Replies Routes
@discussions_bp.route('/<discussion_id>/replies', methods=['GET'])
def get_discussion_replies(discussion_id):
    """Get replies for a discussion"""
    try:
        replies = discussion_controller.get_replies(discussion_id)
        return jsonify(replies), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<discussion_id>/replies', methods=['POST'])
def create_reply(discussion_id):
    """Create a reply to a discussion"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add discussion ID to the data
        data['discussion'] = discussion_id
        
        # Validate data
        validated_data = reply_schema.load(data)
        
        reply = reply_controller.create(validated_data)
        if reply:
            return jsonify(reply), 201
        else:
            return jsonify({'error': 'Failed to create reply'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/replies/<reply_id>', methods=['PUT'])
def update_reply(reply_id):
    """Update a reply"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data (partial update)
        validated_data = reply_schema.load(data, partial=True)
        
        reply = reply_controller.update(reply_id, validated_data)
        if reply:
            return jsonify(reply), 200
        else:
            return jsonify({'error': 'Failed to update reply'}), 500
    
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/replies/<reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    """Delete a reply"""
    try:
        success = reply_controller.delete(reply_id)
        if success:
            return jsonify({'message': 'Reply deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete reply'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
