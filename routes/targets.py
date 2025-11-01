from flask import Blueprint, request, jsonify
from controllers.StudyTargetController import StudyTargetController
from services.pocketbase_service import pocketbase_service
from schemas import StudyTargetSchema
from marshmallow import ValidationError
from utils.auth import require_auth

target_bp = Blueprint('targets', __name__, url_prefix='/api/targets')
study_target_schema = StudyTargetSchema()
target_controller = StudyTargetController(pocketbase_service)

@target_bp.route('/', methods=['GET'])
@require_auth
def get_user_targets():
	"""Get study targets for a specific user"""
	try:
		targets = target_controller.get_user_study_targets() or None
  
		if not targets:
			return jsonify({'error': 'Targets not found'}), 404

		return jsonify({
			"record_id": targets[0].get("id"),
			"daily_target": targets[0].get("daily_target"),
			"weekly_target": targets[0].get("weekly_target"),
			"monthly_target": targets[0].get("monthly_target")
		}), 200

	except Exception as e:
		return jsonify({'error': str(e)}), 500

@target_bp.route('/<record_id>', methods=['PUT'])
@require_auth
def update_user_targets(user_id, record_id):
	"""Update or create study targets for a specific user"""
	try:
		targets = request.get_json()
		if not targets:
			return jsonify({'error': 'No data provided'}), 400

		# Validate data (user and id are optional for validation)
		validated_data = study_target_schema.load(targets, partial=True)

		if not validated_data:
			return jsonify({'error': 'Invalid data'}), 400
		
		if record_id:
			# Update existing record
			updated_targets = target_controller.set_user_study_targets(
				user_id, 
				record_id=record_id, 
				daily_target=validated_data.get("daily_target"),
				weekly_target=validated_data.get("weekly_target"),
				monthly_target=validated_data.get("monthly_target")
			)
		else:
			# Create new record
			new_data = {
				"user": user_id,
				"daily_target": validated_data.get("daily_target", 60),
				"weekly_target": validated_data.get("weekly_target", 300),
				"monthly_target": validated_data.get("monthly_target", 1200)
			}
			updated_targets = target_controller.create(new_data)
  
		return jsonify(updated_targets), 200

	except ValidationError as ve:
		return jsonify({'Validation Error': ve.messages}), 400
	except Exception as e:
		return jsonify({'error': str(e)}), 500