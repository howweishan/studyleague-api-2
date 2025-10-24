from typing import Any, Dict, List
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class StudyRoomController(BaseController):
    """Study room controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "study_rooms")
    
    def get_public_rooms(self) -> List[Dict[str, Any]]:
        """Get all public study rooms"""
        return self.get_all("isPublic = true", "-created", expand="host")
    
    def get_user_rooms(self, user_id: str) -> List[Dict[str, Any]]:
        """Get rooms hosted by a user"""
        return self.get_all(f"host = '{user_id}'", "-created")

