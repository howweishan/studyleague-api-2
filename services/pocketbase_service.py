"""
PocketBase service for simple token-based authentication
Mirrors JavaScript PocketBase SDK behavior
"""

from pocketbase import PocketBase
from pocketbase.errors import ClientResponseError
from typing import Optional, Dict, Any, Union
import os
import json


def serialize_record(record) -> Dict[str, Any]:
    """Helper function to properly serialize PocketBase records including expanded relations"""
    if not record:
        return {}
    
    # Start with the record's dictionary
    result = record.__dict__.copy() if hasattr(record, '__dict__') else {}
    
    # Handle expanded relations recursively
    for key, value in result.items():
        if hasattr(value, '__dict__') and hasattr(value, 'id'):  # It's a Record object
            result[key] = serialize_record(value)
        elif isinstance(value, dict):  # It's a dictionary that might contain Records
            serialized_dict = {}
            for sub_key, sub_value in value.items():
                if hasattr(sub_value, '__dict__') and hasattr(sub_value, 'id'):  # Record object
                    serialized_dict[sub_key] = serialize_record(sub_value)
                else:
                    serialized_dict[sub_key] = sub_value
            result[key] = serialized_dict
        elif isinstance(value, list):  # It's a list that might contain Records
            result[key] = [serialize_record(item) if hasattr(item, '__dict__') and hasattr(item, 'id') else item for item in value]
    
    return result


class PocketBaseService:
	"""Simple PocketBase service that mirrors JavaScript SDK behavior"""
	
	def __init__(self, base_url: Optional[str] = None):
		self.base_url = base_url or os.getenv('POCKETBASE_URL', 'http://127.0.0.1:8090')
		self.pb = PocketBase(self.base_url)
	
	def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
		"""
		Authenticate user with email/password
		Equivalent to: pb.collection("users").authWithPassword(email, password)
		
		Returns:
		{
			'record': user_data,
			'token': auth_token,
			'user_id': user_id,
			'isValid': bool
		}
		"""
		try:
			# Authenticate with PocketBase
			auth_data = self.pb.collection("users").auth_with_password(email, password)
			
			# Return data in JavaScript SDK format
			return {
				'record': serialize_record(auth_data.record),
				'token': auth_data.token,
				'user_id': auth_data.record.id,
				'isValid': bool(self.pb.auth_store.token)
			}
		except ClientResponseError as e:
			return {
				'isValid': False,
				'error': str(e)
			}
	
	def set_auth_token(self, token: str) -> None:
		"""
		Set authentication token manually
		Equivalent to: pb.authStore.save(token, model)
		"""
		self.pb.auth_store.save(token, None)
	
	def get_auth_token(self) -> Optional[str]:
		"""
		Get current authentication token
		Equivalent to: pb.authStore.token
		"""
		return self.pb.auth_store.token
	
	def is_auth_valid(self) -> bool:
		"""
		Check if current authentication is valid
		Equivalent to: pb.authStore.isValid
		"""
		return bool(self.pb.auth_store.token)
	
	def clear_auth(self) -> None:
		"""
		Clear authentication
		Equivalent to: pb.authStore.clear()
		"""
		self.pb.auth_store.clear()
	
	def get_current_user(self) -> Optional[Dict[str, Any]]:
		"""
		Get current authenticated user
		Equivalent to: pb.authStore.model
		"""
		if self.pb.auth_store.model:
			return serialize_record(self.pb.auth_store.model)
		return None
	
	def verify_token(self, token: str) -> Dict[str, Any]:
		"""
		Verify a token and return user info
		"""
		old_token = self.pb.auth_store.token  # Save current token first
		try:
			# Set the token temporarily to verify
			self.pb.auth_store.save(token, None)
			
			# Try to refresh the token to verify it's valid
			auth_data = self.pb.collection("users").auth_refresh()
			
			return {
				'valid': True,
				'user': serialize_record(auth_data.record),
				'user_id': auth_data.record.id
			}
		except ClientResponseError:
			return {'valid': False, 'user': None, 'user_id': None}
		finally:
			# Restore original token
			if old_token is not None:
				self.pb.auth_store.save(old_token, None)
			else:
				self.pb.auth_store.clear()
	
	# Collection access methods (equivalent to pb.collection())
	def get_collection(self, collection_name: str):
		"""Get a PocketBase collection"""
		return self.pb.collection(collection_name)
	
	def create_record(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
		"""Create a record in a collection"""
		try:
			record = self.pb.collection(collection).create(data)
			return serialize_record(record)
		except ClientResponseError as e:
			raise Exception(f"Failed to create record: {e}")
	
	def get_record(self, collection: str, record_id: str, expand: Optional[str] = None) -> Dict[str, Any]:
		"""Get a record by ID"""
		try:
			query_params = {}
			if expand:
				query_params['expand'] = expand
			
			record = self.pb.collection(collection).get_one(record_id, query_params)
			return serialize_record(record)
		except ClientResponseError as e:
			raise Exception(f"Failed to get record: {e}")
		
	def get_records(self, collection: str, filter_query: str = "", sort: str = "", 
					page: int = 1, per_page: int = 30, expand: Optional[str] = None) -> Dict[str, Any]:
		"""Get multiple records with optional filtering, sorting, and pagination"""
		try:
			query_params = {
				'filter': filter_query,
				'sort': sort
			}
			if expand:
				query_params['expand'] = expand
				
			result = self.pb.collection(collection).get_list(
				page=page,
				per_page=per_page,
				query_params=query_params
			)

			return {
				'page': result.page,
				'per_page': result.per_page,
				'total_items': result.total_items,
				'total_pages': result.total_pages,
				'items': [serialize_record(item) for item in result.items]
			}
			
		except ClientResponseError as e:
			raise Exception(f"Failed to get records: {e}")
		except Exception as e:
			raise Exception(f"Failed to get records: {e}")
	
	def update_record(self, collection: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
		"""Update a record"""
		try:
			record = self.pb.collection(collection).update(record_id, data)
			return serialize_record(record)
		except ClientResponseError as e:
			raise Exception(f"Failed to update record: {e}")
	
	def delete_record(self, collection: str, record_id: str) -> bool:
		"""Delete a record"""
		try:
			self.pb.collection(collection).delete(record_id)
			return True
		except ClientResponseError as e:
			raise Exception(f"Failed to delete record: {e}")
	
	def list_records(self, collection: str, page: int = 1, per_page: int = 30, 
					filter_query: str = "", sort: str = "", expand: Optional[str] = None) -> Dict[str, Any]:
		"""List records from a collection"""
		try:
			query_params = {
				'filter': filter_query,
				'sort': sort
			}
			if expand:
				query_params['expand'] = expand
				
			result = self.pb.collection(collection).get_list(
				page=page,
				per_page=per_page,
				query_params=query_params
			)
			
			return {
				'page': result.page,
				'per_page': result.per_page,
				'total_items': result.total_items,
				'total_pages': result.total_pages,
				'items': [serialize_record(item) for item in result.items]
			}
		except ClientResponseError as e:
			raise Exception(f"Failed to list records: {e}")


# Global instance
pocketbase_service = PocketBaseService()