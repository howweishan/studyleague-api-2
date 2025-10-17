#!/usr/bin/env python3
"""
Debug the user achievements query
"""

from services.pocketbase_service import pocketbase_service

def test_user_achievements():
    print("🔄 Testing User Achievements Query...")
    
    # Test different filter syntaxes
    test_user_id = "test_user_123"  # Replace with actual user ID if you have one
    
    print(f"\n1. Testing with spaces: user = '{test_user_id}'")
    try:
        result1 = pocketbase_service.get_records(
            collection="user_achievements",
            filter_query=f"user = '{test_user_id}'",
            sort="-unlockedAt",
            expand="achievement"
        )
        print(f"   Result: {result1['total_items']} items found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n2. Testing without spaces: user='{test_user_id}'")
    try:
        result2 = pocketbase_service.get_records(
            collection="user_achievements", 
            filter_query=f"user='{test_user_id}'",
            sort="-unlockedAt",
            expand="achievement"
        )
        print(f"   Result: {result2['total_items']} items found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n3. Testing with no filter (get all user_achievements)")
    try:
        result3 = pocketbase_service.get_records(
            collection="user_achievements",
            filter_query="",
            sort="-unlockedAt"
        )
        print(f"   Result: {result3['total_items']} total records found")
        if result3['items']:
            print(f"   Sample record: {result3['items'][0]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n4. Testing user collection access")
    try:
        users_result = pocketbase_service.get_records(
            collection="users",
            filter_query="",
            per_page=5
        )
        print(f"   Users found: {users_result['total_items']}")
        if users_result['items']:
            print(f"   Sample user ID: {users_result['items'][0].get('id', 'No ID')}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_user_achievements()
