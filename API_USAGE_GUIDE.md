# StudyLeague API - Multi-User Authentication Guide

## Overview

The StudyLeague API supports multiple users with JWT-based authentication. Each user gets a unique token after login that must be included in subsequent requests.

## Authentication Flow

### 1. User Login
```bash
POST /api/users/auth
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "success": true,
    "user": {
        "id": "abc123def456",
        "email": "user@example.com",
        "name": "John Doe",
        "avatar": null,
        "emailVisibility": false,
        "verified": true,
        "created": "2025-10-15T10:00:00Z",
        "updated": "2025-10-15T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "message": "Authentication successful"
}
```

### 2. Using the Token

Include the JWT token in the Authorization header for all subsequent requests:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## API Endpoints with Authentication

### User Management

#### Get Current User Profile
```bash
GET /api/users/me
Authorization: Bearer <your-jwt-token>
```

#### Get Any User Profile
```bash
GET /api/users/<user_id>
Authorization: Bearer <your-jwt-token>
```

### Study Sessions

#### Get Your Sessions
```bash
GET /api/sessions/
Authorization: Bearer <your-jwt-token>
```

#### Get Active Sessions Only
```bash
GET /api/sessions/?active=true
Authorization: Bearer <your-jwt-token>
```

#### Create a Study Session
```bash
POST /api/sessions/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "durationMinutes": 60,
    "active": true,
    "room": "room_id_optional"
}
```

Note: The `user` field is automatically set to the authenticated user.

#### Update a Session
```bash
PUT /api/sessions/<session_id>
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "durationMinutes": 90,
    "active": false,
    "integrityScore": 85.5
}
```

#### End a Session
```bash
POST /api/sessions/<session_id>/end
Authorization: Bearer <your-jwt-token>
```

### Study Rooms

#### Get Public Rooms
```bash
GET /api/rooms/?public=true
Authorization: Bearer <your-jwt-token>
```

#### Create a Study Room
```bash
POST /api/rooms/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "roomName": "Math Study Group",
    "maxParticipants": 10,
    "isPublic": true,
    "host": "your_user_id"
}
```

### Discussions

#### Get All Discussions
```bash
GET /api/discussions/
Authorization: Bearer <your-jwt-token>
```

#### Create a Discussion
```bash
POST /api/discussions/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "title": "Study Tips for Calculus",
    "content": "What are your best tips for studying calculus?",
    "author": "your_user_id"
}
```

#### Reply to a Discussion
```bash
POST /api/discussions/<discussion_id>/replies
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "body": "I find practicing derivatives daily really helps!",
    "author": "your_user_id"
}
```

### Achievements

#### Get All Available Achievements
```bash
GET /api/achievements/
Authorization: Bearer <your-jwt-token>
```

#### Get User's Achievements
```bash
GET /api/achievements/user/<user_id>
Authorization: Bearer <your-jwt-token>
```

#### Unlock an Achievement
```bash
POST /api/achievements/unlock
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
    "user": "your_user_id",
    "achievement": "achievement_id"
}
```

### Leaderboard

#### Get Top Users
```bash
GET /api/leaderboard/?limit=10
Authorization: Bearer <your-jwt-token>
```

## Example Client Implementation (JavaScript)

```javascript
class StudyLeagueAPI {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('studyleague_token');
    }

    async login(email, password) {
        const response = await fetch(`${this.baseURL}/api/users/auth`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (data.success) {
            this.token = data.token;
            localStorage.setItem('studyleague_token', this.token);
            return data;
        }
        throw new Error(data.error);
    }

    async apiCall(endpoint, method = 'GET', body = null) {
        const headers = {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        };

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        return response.json();
    }

    // User methods
    async getCurrentUser() {
        return this.apiCall('/api/users/me');
    }

    // Session methods
    async createSession(sessionData) {
        return this.apiCall('/api/sessions/', 'POST', sessionData);
    }

    async getMySessions() {
        return this.apiCall('/api/sessions/');
    }

    async endSession(sessionId) {
        return this.apiCall(`/api/sessions/${sessionId}/end`, 'POST');
    }

    // Room methods
    async getPublicRooms() {
        return this.apiCall('/api/rooms/?public=true');
    }

    async createRoom(roomData) {
        return this.apiCall('/api/rooms/', 'POST', roomData);
    }

    // Discussion methods
    async getDiscussions() {
        return this.apiCall('/api/discussions/');
    }

    async createDiscussion(discussionData) {
        return this.apiCall('/api/discussions/', 'POST', discussionData);
    }

    // Leaderboard
    async getLeaderboard(limit = 10) {
        return this.apiCall(`/api/leaderboard/?limit=${limit}`);
    }
}

// Usage example
const api = new StudyLeagueAPI();

// Login
api.login('user@example.com', 'password123')
    .then(data => {
        console.log('Logged in:', data.user);
        
        // Create a study session
        return api.createSession({
            durationMinutes: 60,
            active: true
        });
    })
    .then(session => {
        console.log('Session created:', session);
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
```

## Security Features

1. **JWT Tokens**: Secure, stateless authentication
2. **Token Expiration**: Tokens expire after 24 hours
3. **User Isolation**: Users can only access their own data
4. **PocketBase Integration**: Respects PocketBase's built-in access rules
5. **Authorization Headers**: Standard Bearer token format

## Error Handling

All endpoints return consistent error responses:

```json
{
    "error": "Error message description"
}
```

Common HTTP status codes:
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (access denied)
- `404` - Not Found
- `500` - Internal Server Error

## Multi-User Support

The API fully supports multiple users:
- Each user has their own isolated data
- Sessions are user-specific
- Rooms can be public or private
- Discussions are shared but authored by specific users
- Achievements are tracked per user
- Leaderboard shows all users (public data)

Users cannot access each other's private data without proper authorization.
