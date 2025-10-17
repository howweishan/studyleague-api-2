#!/usr/bin/env python3
"""
Quick check to verify PocketBase service is working
"""

from services.pocketbase_service import pocketbase_service

def test_service():
    print("🔄 Testing PocketBase Service...")
    print(f"   Service URL: {pocketbase_service.base_url}")
    print(f"   Auth Token: {pocketbase_service.get_auth_token() or 'None'}")
    print(f"   Auth Valid: {pocketbase_service.is_auth_valid()}")
    
    # Try to get collections list
    try:
        # Simple test - try to access users collection
        users_collection = pocketbase_service.get_collection("users")
        print(f"✅ Successfully connected to PocketBase")
        print(f"   Users collection: {users_collection}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Make sure PocketBase is running on http://127.0.0.1:8090")

if __name__ == "__main__":
    test_service()
