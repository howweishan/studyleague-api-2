#!/usr/bin/env python3
"""
Test script for StudyLeague API multi-user functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

class StudyLeagueAPITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
        
    def login(self, email, password):
        """Login and store the JWT token"""
        url = f"{self.base_url}/api/users/auth"
        data = {"email": email, "password": password}
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.token = result['token']
            print(f"✅ Logged in as: {result['user']['email']}")
            return result
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    
    def make_request(self, endpoint, method="GET", data=None):
        """Make authenticated request to the API"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return None
            
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        return response
    
    def test_current_user(self):
        """Test getting current user profile"""
        response = self.make_request("/api/users/me")
        if response and response.status_code == 200:
            user = response.json()
            print(f"✅ Current user: {user['email']}")
            return user
        else:
            print(f"❌ Failed to get current user: {response.json() if response else 'No response'}")
            return None
    
    def test_create_session(self):
        """Test creating a study session"""
        data = {
            "durationMinutes": 30,
            "active": True
        }
        response = self.make_request("/api/sessions/", "POST", data)
        if response and response.status_code == 201:
            session = response.json()
            print(f"✅ Created session: {session['id']}")
            return session
        else:
            print(f"❌ Failed to create session: {response.json() if response else 'No response'}")
            return None
    
    def test_get_sessions(self):
        """Test getting user's sessions"""
        response = self.make_request("/api/sessions/")
        if response and response.status_code == 200:
            sessions = response.json()
            print(f"✅ Found {len(sessions)} sessions")
            return sessions
        else:
            print(f"❌ Failed to get sessions: {response.json() if response else 'No response'}")
            return None
    
    def test_create_room(self):
        """Test creating a study room"""
        data = {
            "roomName": "Test Study Room",
            "maxParticipants": 5,
            "isPublic": True,
            "host": "test_user_id"  # This should be set automatically by the API
        }
        response = self.make_request("/api/rooms/", "POST", data)
        if response and response.status_code == 201:
            room = response.json()
            print(f"✅ Created room: {room['roomName']}")
            return room
        else:
            print(f"❌ Failed to create room: {response.json() if response else 'No response'}")
            return None

def main():
    print("🚀 Testing StudyLeague API Multi-User Functionality")
    print("=" * 50)
    
    # Test with first user
    print("\n👤 Testing User 1:")
    user1 = StudyLeagueAPITester()
    
    # Note: You'll need to create test users in your PocketBase instance first
    # For demo purposes, using the admin credentials
    login_result = user1.login("guest@guest.org", "guest1234")
    
    if login_result:
        user1.test_current_user()
        user1.test_create_session()
        user1.test_get_sessions()
        # user1.test_create_room()  # Uncomment if room creation is working
    
    print("\n" + "=" * 50)
    print("✅ Multi-user API testing completed!")
    print("\nTo test with multiple users:")
    print("1. Create additional users in PocketBase")
    print("2. Update this script with their credentials")
    print("3. Test that users can only access their own data")

if __name__ == "__main__":
    main()
