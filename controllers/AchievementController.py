from typing import Any, Dict, List, Optional
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class AchievementController(BaseController):
    """Achievement controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "achievements")
    
    def get_all_achievements(self) -> List[Dict[str, Any]]:
        """Get all available achievements"""
        return self.get_all("", "title")
    
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