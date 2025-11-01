from typing import Any, Dict, List
from .BaseController import BaseController
from services.pocketbase_service import PocketBaseService

class LeaderboardController(BaseController):
    """Leaderboard controller"""
    
    def __init__(self, pb_service: PocketBaseService):
        super().__init__(pb_service, "leaderboard")
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard top users"""
        return self.get_all(filter_query="", sort="-total_day", per_page=limit, expand="user")