from typing import Any, Dict, List
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService



class StatisticsController(BaseController):
	"""Statistics controller"""

	def __init__(self, pb_service: PocketBaseService):
		super().__init__(pb_service, "study_rooms")
	
	def get_user_total_study_time(self, user_id: str) -> List[Dict[str, Any]]:
		"""Get user rank based on total study time"""
		result = self.get_all(f"user = '{user_id}'", "")
		return result