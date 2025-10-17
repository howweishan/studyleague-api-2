# StudyLeague API

A Flask-based REST API for the StudyLeague application, integrating with PocketBase as the backend database. **Now with full multi-user support and JWT authentication!**

## Features

- **🔐 Multi-User Authentication**: JWT-based authentication with user isolation
- **👤 User Management**: Secure login, profile management, and user-specific data
- **📚 Study Sessions**: Track study time and progress per user
- **🏠 Study Rooms**: Create and join collaborative study spaces
- **🏆 Achievements**: Gamification system with unlockable achievements per user
- **💬 Discussions**: Community discussion forum with user-specific authoring
- **📊 Leaderboard**: Track top performers by study time
- **🎯 Object-Oriented Architecture**: Clean separation of concerns with models, controllers, and services
- **🔒 Access Control**: Users can only access their own data (with proper authorization)

## Multi-User Support

✅ **Full multi-user functionality with session management:**
- Each user receives a unique JWT token upon login
- All API requests require authentication via `Authorization: Bearer <token>` header
- Users can only access their own study sessions, achievements, and private data
- Public data (discussions, public rooms, leaderboard) is shared across users
- Token-based stateless authentication for scalability

## Architecture

### Project Structure
```
studyleague-api-2/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── models/
│   └── __init__.py       # Data models and schemas
├── services/
│   └── pocketbase_service.py  # PocketBase integration
├── controllers/
│   └── __init__.py       # Business logic controllers
├── routes/
│   ├── users.py          # User-related endpoints
│   ├── sessions.py       # Study session endpoints
│   ├── rooms.py          # Study room endpoints
│   ├── achievements.py   # Achievement endpoints
│   ├── discussions.py    # Discussion endpoints
│   └── leaderboard.py    # Leaderboard endpoints
└── schemas/
    └── __init__.py       # Data validation schemas
```

### Components

1. **Models**: Data classes representing PocketBase collections
2. **Services**: PocketBase integration and database operations
3. **Controllers**: Business logic for each domain
4. **Routes**: REST API endpoints
5. **Schemas**: Data validation using Marshmallow

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
POCKETBASE_URL=http://localhost:8090
POCKETBASE_ADMIN_EMAIL=guest@guest.org
POCKETBASE_ADMIN_PASSWORD=guest1234
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this
```

3. Ensure PocketBase is running on localhost:8090

## Usage

Run the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/users/auth` - Login and receive JWT token

### Users
- `GET /api/users/me` - Get current user profile (requires auth)
- `GET /api/users/<user_id>` - Get user profile (requires auth)
- `GET /api/users/` - Get all users (requires auth)
- `POST /api/users/` - Create user
- `PUT /api/users/<user_id>` - Update user (requires auth)
- `DELETE /api/users/<user_id>` - Delete user (requires auth)

### Study Sessions (All require authentication)
- `GET /api/sessions/` - Get your study sessions
- `GET /api/sessions/?active=true` - Get active sessions only
- `GET /api/sessions/<session_id>` - Get session by ID (if you own it)
- `POST /api/sessions/` - Create study session (auto-assigns to current user)
- `PUT /api/sessions/<session_id>` - Update session (if you own it)
- `POST /api/sessions/<session_id>/end` - End session (if you own it)
- `DELETE /api/sessions/<session_id>` - Delete session (if you own it)

### Study Rooms (All require authentication)
- `GET /api/rooms/` - Get study rooms
- `GET /api/rooms/?public=true` - Get public rooms only
- `GET /api/rooms/?host_id=<user_id>` - Get rooms by host
- `GET /api/rooms/<room_id>` - Get room by ID
- `POST /api/rooms/` - Create study room
- `PUT /api/rooms/<room_id>` - Update room (if you're the host)
- `DELETE /api/rooms/<room_id>` - Delete room (if you're the host)

### Achievements (All require authentication)
- `GET /api/achievements/` - Get all achievements
- `GET /api/achievements/<achievement_id>` - Get achievement by ID
- `GET /api/achievements/user/<user_id>` - Get user achievements
- `POST /api/achievements/unlock` - Unlock achievement
- `POST /api/achievements/` - Create achievement (admin)
- `PUT /api/achievements/<achievement_id>` - Update achievement (admin)
- `DELETE /api/achievements/<achievement_id>` - Delete achievement (admin)

### Discussions (All require authentication)
- `GET /api/discussions/` - Get all discussions
- `GET /api/discussions/<discussion_id>` - Get discussion by ID
- `POST /api/discussions/` - Create discussion
- `PUT /api/discussions/<discussion_id>` - Update discussion (if you're author)
- `DELETE /api/discussions/<discussion_id>` - Delete discussion (if you're author)
- `GET /api/discussions/<discussion_id>/replies` - Get discussion replies
- `POST /api/discussions/<discussion_id>/replies` - Create reply
- `PUT /api/discussions/replies/<reply_id>` - Update reply (if you're author)
- `DELETE /api/discussions/replies/<reply_id>` - Delete reply (if you're author)

### Leaderboard (Requires authentication)
- `GET /api/leaderboard/` - Get leaderboard

## Authentication Usage

1. **Login** to get your token:
```bash
POST /api/users/auth
{
    "email": "user@example.com",
    "password": "password123"
}
```

2. **Include token** in all subsequent requests:
```bash
Authorization: Bearer <your-jwt-token>
```

3. **Example authenticated request**:
```bash
GET /api/sessions/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## PocketBase Integration

The API uses the PocketBase Python SDK to interact with your PocketBase instance. The service layer handles:

- Authentication with admin credentials
- CRUD operations on all collections
- Relationship expansion
- Error handling

## Development

The application uses Flask's development server with hot reloading enabled. For production deployment, use a WSGI server like Gunicorn.

## Error Handling

All endpoints include comprehensive error handling with appropriate HTTP status codes and JSON error responses.
