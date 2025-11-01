from flask import Blueprint, request, jsonify
from controllers import StudySessionController, StatisticsController
from services.pocketbase_service import pocketbase_service
from schemas import StudySessionSchema
from marshmallow import ValidationError
from utils.auth import require_auth

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/', methods=['GET'], strict_slashes=False)
@require_auth
def get_today_statistics():
	"""Get today's statistics"""
	try:
		statistics_controller = StatisticsController(pocketbase_service)
		stats = statistics_controller.get_today_statistics()
		return jsonify(stats), 200
	
	except Exception as e:
		return jsonify({'error': str(e)}), 500