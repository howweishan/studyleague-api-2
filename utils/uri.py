import os
base_url = os.getenv('PROD_POCKETBASE_URL', 'http://127.0.0.1:8090')

# casted from ${POCKETBASE_URL}/api/files/study_rooms/${room.id}/${room.thumbnail}`
def cast_image_uri(file_name: str, collection_name: str, record_id: str) -> str:
    """Construct full URI for accessing a file in PocketBase"""
    return f"{base_url}/api/files/{collection_name}/{record_id}/{file_name}"