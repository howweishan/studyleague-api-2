from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from services.pocketbase_service import PocketBaseService

class BaseController(ABC):
    """Base controller class"""
    
    def __init__(self, pb_service: PocketBaseService, collection_name: str):
        self.pb_service = pb_service
        self.collection_name = collection_name
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new record"""
        return self.pb_service.create_record(self.collection_name, data)
    
    def get_by_id(self, record_id: str, expand: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get record by ID"""
        return self.pb_service.get_record(self.collection_name, record_id, expand)
    
    def get_all(self, filter_query: str = "", sort: str = "", 
               page: int = 1, per_page: int = 30, expand: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all records with optional filtering"""
        result = self.pb_service.get_records(self.collection_name, filter_query, sort, page, per_page, expand)
        
        # Extract just the items from the paginated result
        return result.get('items', []) if isinstance(result, dict) else result
    
    def update(self, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record"""
        return self.pb_service.update_record(self.collection_name, record_id, data)
    
    def delete(self, record_id: str) -> bool:
        """Delete a record"""
        return self.pb_service.delete_record(self.collection_name, record_id)

class UserController(BaseController):
    """User controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "users")
    
    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user"""
        return self.pb_service.authenticate_user(email, password)
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile with avatar"""
        return self.get_by_id(user_id, "avatar")

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
    
    def end_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """End a study session"""
        return self.update(session_id, {"active": False})

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

class AchievementController(BaseController):
    """Achievement controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "achievements")
    
    def get_all_achievements(self) -> List[Dict[str, Any]]:
        """Get all available achievements"""
        return self.get_all("", "title")

class UserAchievementController(BaseController):
    """User achievement controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "user_achievements")
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get achievements for a user"""
        return self.get_all(filter_query=f"user = '{user_id}'", sort="-unlockedAt", expand="achievement")
    
    def unlock_achievement(self, user_id: str, achievement_id: str) -> Optional[Dict[str, Any]]:
        """Unlock an achievement for a user"""
        data = {
            "user": user_id,
            "achievement": achievement_id
        }
        return self.create(data)

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

class LeaderboardController(BaseController):
    """Leaderboard controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "leaderboard")
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard top users"""
        return self.get_all("", "-monthTotal", per_page=limit, expand="user")
