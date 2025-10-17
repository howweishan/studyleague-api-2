# StudyLeague API - Simple PocketBase Token Usage

## Overview

The API now uses PocketBase tokens directly, just like the JavaScript SDK. No custom JWT tokens needed!

## JavaScript Reference (from your example)
```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// Login and get token
const authData = await pb.collection("users").authWithPassword('test@example.com', '1234567890');

// After login, you can access:
console.log(pb.authStore.isValid);  // true
console.log(pb.authStore.token);    // "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
console.log(pb.authStore.record.id); // "user_id_here"

// Logout
pb.authStore.clear();
```

## Python Equivalent

### 1. Login (Python)
```bash
POST /api/users/auth
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "1234567890"
}
```

**Response:**
```json
{
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "user_id_here",
        "email": "test@example.com",
        "name": "Test User",
        "verified": true,
        "created": "2025-10-15T10:00:00Z",
        "updated": "2025-10-15T10:00:00Z"
    },
    "isValid": true,
    "user_id": "user_id_here",
    "message": "Authentication successful"
}
```

### 2. Use Token in Subsequent Requests
```bash
GET /api/sessions/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Logout (Python)
```bash
POST /api/users/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Python Client Example

```python
import requests

class StudyLeagueClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.user = None
    
    def login(self, email, password):
        """Login and store token - equivalent to pb.collection("users").authWithPassword()"""
        response = requests.post(f"{self.base_url}/api/users/auth", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']  # This is pb.authStore.token
            self.user = data['user']    # This is pb.authStore.record
            print(f"Login successful! Token: {self.token[:20]}...")
            print(f"User ID: {data['user_id']}")  # This is pb.authStore.record.id
            print(f"Auth Valid: {data['isValid']}")  # This is pb.authStore.isValid
            return data
        else:
            print(f"Login failed: {response.json()}")
            return None
    
    def logout(self):
        """Logout - equivalent to pb.authStore.clear()"""
        if self.token:
            response = requests.post(f"{self.base_url}/api/users/logout", 
                                   headers={"Authorization": f"Bearer {self.token}"})
            self.token = None
            self.user = None
            print("Logged out successfully")
    
    def get_sessions(self, user_id=None):
        """Get study sessions"""
        if not self.token:
            print("Not logged in")
            return None
        
        params = {"user_id": user_id} if user_id else {}
        response = requests.get(f"{self.base_url}/api/sessions/", 
                              headers={"Authorization": f"Bearer {self.token}"},
                              params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get sessions: {response.json()}")
            return None
    
    def create_session(self, duration_minutes=60, active=True, room=None):
        """Create a study session"""
        if not self.token:
            print("Not logged in")
            return None
        
        session_data = {
            "user": self.user['id'],  # Set user from logged in user
            "durationMinutes": duration_minutes,
            "active": active
        }
        if room:
            session_data["room"] = room
        
        response = requests.post(f"{self.base_url}/api/sessions/", 
                               headers={"Authorization": f"Bearer {self.token}"},
                               json=session_data)
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create session: {response.json()}")
            return None

# Usage example
if __name__ == "__main__":
    client = StudyLeagueClient()
    
    # Login (equivalent to JavaScript authWithPassword)
    auth_data = client.login("guest@guest.org", "guest1234")
    
    if auth_data:
        # Create a session
        session = client.create_session(duration_minutes=30)
        if session:
            print(f"Created session: {session['id']}")
        
        # Get sessions
        sessions = client.get_sessions()
        if sessions:
            print(f"Found {len(sessions)} sessions")
        
        # Logout (equivalent to pb.authStore.clear())
        client.logout()
```

## Key Changes Made

1. **Removed Custom JWT**: No more custom JWT tokens
2. **Direct PocketBase Tokens**: Uses PocketBase's built-in auth tokens
3. **Simple Token Passing**: Just pass the token in Authorization header
4. **JavaScript Equivalent**: Mirrors the JavaScript PocketBase SDK behavior
5. **No Complex Auth Service**: Uses PocketBase's auth store directly

## Multi-User Support

✅ **Yes, it still supports multiple users!**
- Each user gets their own PocketBase token when they login
- Tokens are unique per user session
- Multiple users can be logged in simultaneously with different tokens
- Each request uses the user's specific token

The difference is now we're using PocketBase's native token system instead of creating custom JWT tokens on top of it.
