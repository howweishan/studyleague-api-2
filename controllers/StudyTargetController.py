from typing import Any, Dict, List, Optional
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class StudyTargetController(BaseController):
	"""Study target controller"""
	
	def __init__(self, pb_service: PocketBaseService):
		super().__init__(pb_service, "study_targets")
	
	def get_user_study_targets(self) -> List[Dict[str, Any]]:
		"""Get all study targets for a user"""
		return self.get_all(f"", "created")

	def set_user_study_targets(self, user_id: str, record_id: str, daily_target:int, weekly_target:int, monthly_target:int) -> Optional[Dict[str, Any]]:
		"""Set study targets for a user"""
		data = {
			"user": user_id,
			"daily_target": daily_target,
			"weekly_target": weekly_target,
			"monthly_target": monthly_target
		}
		return self.update(record_id, data)