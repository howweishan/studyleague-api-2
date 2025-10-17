from flask import Blueprint, request, jsonify
from controllers import LeaderboardController
from services.pocketbase_service import pocketbase_service
from utils.auth import require_auth, get_auth_token_from_header

# Use the global service instance
leaderboard_controller = LeaderboardController(pocketbase_service)

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')

@leaderboard_bp.route('/', methods=['GET'])
@require_auth
def get_leaderboard():
    """Get leaderboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        leaderboard = leaderboard_controller.get_leaderboard(limit)
        return jsonify(leaderboard), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
