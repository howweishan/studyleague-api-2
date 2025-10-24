from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService
from typing import Any, Dict, Optional

class UserController(BaseController):
	"""User controller"""
	
	def __init__(self, pb_service: PocketBaseService):
		super().__init__(pb_service, "users")
	
	def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
		"""Authenticate user"""
		return self.pb_service.authenticate(email, password)
	
	def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
		"""Get user profile with avatar and apply schema"""

		from schemas import UserSchema

		data = self.get_by_id(user_id, "avatar")
		if not data:
			return None

		# Create schema instance and dump the data
		try:
			schema = UserSchema()
			result = schema.dump(data)
   
			# Ensure we return a Dict[str, Any]
			return result if isinstance(result, dict) else data

		except Exception:
			# If schema validation fails, fall back to raw data
			return data
