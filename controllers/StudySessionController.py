from typing import Any, Dict, List, Optional
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class StudySessionController(BaseController):
	"""Study session controller"""
	
	def __init__(self, pb_service: PocketBaseService):
		super().__init__(pb_service, "study_sessions")
	
	def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
		"""Get all sessions for a user"""
		return self.get_all(f"user = '{user_id}'", "-startedAt", expand="room")
	
	def get_active_sessions(self, user_id: str) -> List[Dict[str, Any]]:
		"""Get active sessions for a user"""
		return self.get_all(f"user = '{user_id}' && active = true", "-startedAt")

	
	def start_study_session(self, user_id: str, room_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
		"""Start a new study session"""
		data = {
			"user": user_id,
			"room": room_id,
			"startedAt": None,
			"endedAt": None,
			"durationMinutes": 0,
			"active": True
		}
		return self.create(data)
	
	def end_session(self, session_id: str) -> Optional[Dict[str, Any]]:
		"""End a study session"""
		return self.update(session_id, {"active": False, "endedAt": None})
