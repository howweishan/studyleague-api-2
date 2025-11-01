"""
Shared authentication utilities for routes
"""

from functools import wraps
from flask import request, jsonify
from services.pocketbase_service import pocketbase_service
import inspect


def require_auth(f):
    """Decorator to require authentication for a route and optionally inject user_id"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            # Set the auth token for this request
            pocketbase_service.set_auth_token(token)
            
            # Verify the token is valid and get user info
            if not pocketbase_service.is_auth_valid():
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Get the authenticated user's ID from the auth store
            user_id = pocketbase_service.get_auth_user_id()
            
            if not user_id:
                return jsonify({'error': 'Unable to retrieve user information'}), 401
            
            # Check if the function expects a user_id parameter
            sig = inspect.signature(f)
            params = list(sig.parameters.keys())
            
            # If function expects user_id as first parameter, inject it
            if params and params[0] == 'user_id':
                return f(user_id, *args, **kwargs)
            else:
                # Otherwise, just call the function normally (user can get ID via get_current_user if needed)
                return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401
        finally:
            # Clear auth after request (optional, for security)
            # pocketbase_service.clear_auth()
            pass
    
    return decorated_function

def get_auth_token_from_header():
    """Helper function to extract and set auth token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        pocketbase_service.set_auth_token(token)
        return token
    return None

def ensure_authenticated():
    """Ensure the current request is authenticated, return user info if valid"""
    token = get_auth_token_from_header()
    if not token:
        return None, jsonify({'error': 'Authorization token required.'}), 401
    
    try:
        # Verify token and get user info
        verification = pocketbase_service.verify_token(token)
        if verification.get('valid'):
            return verification.get('user'), None, None
        else:
            return None, jsonify({'error': 'Invalid token. Please log in again.'}), 401
    except Exception as e:
        return None, jsonify({'error': f'Authentication failed: {str(e)}'}), 401
