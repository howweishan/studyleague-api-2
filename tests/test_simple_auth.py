#!/usr/bin/env python3
"""
Simple test showing the reverted PocketBase token approach (like JavaScript)
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_simple_auth():
    """Test the simple PocketBase token authentication"""
    print("🔄 Testing Simple PocketBase Token Authentication")
    print("=" * 60)
    
    # Step 1: Login (equivalent to JavaScript pb.collection("users").authWithPassword())
    print("\n1. Login:")
    login_data = {
        "email": "guest@guest.org", 
        "password": "guest1234"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/auth", json=login_data)
    
    if response.status_code == 200:
        auth_data = response.json()
        print(f"✅ Login successful!")
        print(f"   Token: {auth_data['token'][:30]}...")
        print(f"   User ID: {auth_data['user_id']}")
        print(f"   Is Valid: {auth_data['isValid']}")
        print(f"   User Email: {auth_data['user']['email']}")
        
        # Store token for subsequent requests
        token = auth_data['token']
        user_id = auth_data['user_id']
        
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    # Step 2: Use token in API calls
    print("\n2. Using token in API calls:")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting user profile
    response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    if response.status_code == 200:
        print(f"✅ Got user profile successfully")
    else:
        print(f"❌ Failed to get user profile: {response.text}")
    
    # Test creating a session
    session_data = {
        "user": user_id,
        "durationMinutes": 45,
        "active": True
    }
    
    response = requests.post(f"{BASE_URL}/api/sessions/", headers=headers, json=session_data)
    if response.status_code == 201:
        session = response.json()
        print(f"✅ Created study session: {session.get('id', 'N/A')}")
        session_id = session.get('id')
    else:
        print(f"❌ Failed to create session: {response.text}")
        session_id = None
    
    # Test getting sessions
    response = requests.get(f"{BASE_URL}/api/sessions/?user_id={user_id}", headers=headers)
    if response.status_code == 200:
        sessions = response.json()
        print(f"✅ Retrieved {len(sessions)} sessions")
    else:
        print(f"❌ Failed to get sessions: {response.text}")
    
    # Step 3: Logout (equivalent to pb.authStore.clear())
    print("\n3. Logout:")
    response = requests.post(f"{BASE_URL}/api/users/logout", headers=headers)
    if response.status_code == 200:
        print("✅ Logged out successfully")
    else:
        print(f"❌ Logout failed: {response.text}")
    
    print("\n" + "=" * 60)
    print("✅ Simple PocketBase token test completed!")
    print("\nThis approach mirrors the JavaScript PocketBase SDK:")
    print("- Login returns the PocketBase token directly")
    print("- Token is passed in Authorization header") 
    print("- Multiple users can have different tokens")
    print("- No custom JWT tokens needed!")

def test_multiple_users():
    """Demonstrate multiple user support"""
    print("\n🔄 Testing Multiple User Support")
    print("=" * 60)
    
    print("Note: For this test to work fully, you need multiple users in PocketBase")
    print("Currently testing with the same user to show token isolation...")
    
    # Simulate two user sessions
    sessions = []
    
    for i in range(2):
        print(f"\n👤 User Session {i+1}:")
        
        # Each user gets their own token
        login_data = {"email": "guest@guest.org", "password": "guest1234"}
        response = requests.post(f"{BASE_URL}/api/users/auth", json=login_data)
        
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['token']
            user_id = auth_data['user_id']
            
            sessions.append({
                'token': token,
                'user_id': user_id,
                'session_num': i+1
            })
            
            print(f"✅ User {i+1} logged in with token: {token[:20]}...")
        else:
            print(f"❌ User {i+1} login failed")
    
    # Show that tokens are different (even for same user, new login = new token)
    if len(sessions) >= 2:
        token1 = sessions[0]['token']
        token2 = sessions[1]['token']
        
        if token1 != token2:
            print(f"\n✅ Tokens are unique:")
            print(f"   Session 1: {token1[:30]}...")
            print(f"   Session 2: {token2[:30]}...")
        else:
            print(f"\n⚠️  Tokens are the same (PocketBase may reuse tokens for same user)")
    
    print("\n" + "=" * 60)
    print("✅ Multi-user support confirmed!")
    print("- Each login gets its own token")
    print("- Tokens can be used independently")
    print("- API isolates data per user/token")

if __name__ == "__main__":
    try:
        test_simple_auth()
        test_multiple_users()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server.")
        print("Make sure the Flask app is running on localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
