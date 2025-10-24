from flask import Blueprint, request, jsonify
from controllers import StudySessionController
from services.pocketbase_service import pocketbase_service
from schemas import StudySessionSchema
from marshmallow import ValidationError
from utils.auth import require_auth, get_auth_token_from_header

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/user/<user_id>', methods=['GET'])
@require_auth
def get_user_statistics(user_id):
	"""Get statistics for a specific user"""
	try:
		session_controller = StudySessionController(pocketbase_service)
		stats = session_controller.get_user_statistics(user_id)
		return jsonify(stats), 200
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500