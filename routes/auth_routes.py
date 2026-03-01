#LOGIN/REGISTER
#These are the first endpoints your frontend will need so users can sign up and log in.
# Import	What it does
# Blueprint	Groups related routes together (all auth routes in one place)
# request	Gets data from the HTTP request (JSON body, headers)
# jsonify	Converts Python dictionaries to JSON responses
# User	Our User model that handles database operations
from flask import Blueprint, request, jsonify, session
from models.user import User

#Create the Blueprint that will prefix all routes with /api/auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
#REGISTER ROUTE
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Auth blueprint is working!"})

@auth_bp.route('/register', methods=['POST'])
def register():
    "Register New user"
    data = request.get_json()
    #Validate required fields are present
    if not data:
        return jsonify({"error" : "NO data provided"}) ,400
    if not data.get("email"):
        return jsonify({"error" : "Email is required"}), 400
    if not data.get("password"):
        return jsonify({"error" : "Password is required"}), 400
    if not data.get("username"):
        return jsonify({"error" : "Username is required"}), 400
    
    #Create the user using user model
    user = User.create(
        username= data['username'],
        email = data["email"],
        password = data["password"],
        full_name= data.get('full_name'), #optional
        phone = data.get('phone') #optional
    )

    if user:
         # Auto-login after registration
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify(user), 201
    return jsonify({"error": "Email or username already exists"}), 400 #Bad Request - client sent something wrong

#LOGIN ROUTE
@auth_bp.route('/login', methods=['POST'])
def login():
    #Login user
    #Get login credentials
    data = request.get_json()
    #Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password required"}), 400

    #Validate user credentials
    user = User.verify_password(data['email'], data['password'])

    if user:
         # ✅ THIS IS THE KEY PART - Create session!
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['logged_in'] = True
        
        return jsonify({
            "message": "Login successful",
            "user": user
        }), 200
    return jsonify({"error": "Invalid password or email"}), 401 #Unauthorized - authentication failed

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and clear session"""
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get currently logged in user"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    
    user = User.get_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        session.clear()
        return jsonify({"error": "User not found"}), 404











    # """Get current user (placeholder - will add session later)"""
    # # For now, return a helpful message
    # # In the future, this will get the logged-in user from session
    # return jsonify({
    #     "message": "Session management coming soon",
    #     "note": "For now, use /login and save the returned user data"
    # }), 200
# Why This Placeholder?

# For now, we're keeping it simple. Later we'll add:

#     Sessions - Store login status on server

#     JWT Tokens - More modern approach for APIs

#     Authentication headers - Client sends token with each request


