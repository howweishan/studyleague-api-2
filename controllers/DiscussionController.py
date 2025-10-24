from typing import Any, Dict, List
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class DiscussionController(BaseController):
    """Discussion controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "discussions")
    
    def get_all_discussions(self) -> List[Dict[str, Any]]:
        """Get all discussions"""
        return self.get_all("", "-created", expand="author")
    
    def get_user_discussions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get discussions by a user"""
        return self.get_all(f"author = '{user_id}'", "-created")

class DiscussionReplyController(BaseController):
    """Discussion reply controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "discussion_replies")
    
    def get_discussion_replies(self, discussion_id: str) -> List[Dict[str, Any]]:
        """Get replies for a discussion"""
        return self.get_all(f"discussion = '{discussion_id}'", "created", expand="author")

