# auth_helpers.py (login required decorator)
from functools import wraps
from flask import session, jsonify, request
from models.user import User

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is in session
        user_id = session.get('user_id')
        
        if not user_id:
            # Also check for token in header (for API clients)
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # You could validate JWT token here
                # For now, we'll just use session
                pass
            
            return jsonify({"error": "Authentication required"}), 401
        
        # Get user from database
        user = User.get_by_id(user_id)
        if not user:
            session.clear()
            return jsonify({"error": "User not found"}), 401
        
        # Attach user to request for easy access
        request.current_user = user
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if logged in
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Check if user is admin
        user = User.get_by_id(user_id)
        if not user or not user.get('is_admin'):
            return jsonify({"error": "Admin privileges required"}), 403
        
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Helper to get current user from session"""
    user_id = session.get('user_id')
    if user_id:
        return User.get_by_id(user_id)
    return None