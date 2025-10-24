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
        result = self.pb_service.list_records(self.collection_name, page, per_page, filter_query, sort, expand)
        
        # Extract just the items from the paginated result
        return result.get('items', []) if isinstance(result, dict) else result
    
    def update(self, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record"""
        return self.pb_service.update_record(self.collection_name, record_id, data)
    
    def delete(self, record_id: str) -> bool:
        """Delete a record"""
        return self.pb_service.delete_record(self.collection_name, record_id)

