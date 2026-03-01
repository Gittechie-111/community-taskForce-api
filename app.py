#MAIN APPLICATION
# app.py
import os
from dotenv import load_dotenv

# Load .env file IMMEDIATELY
load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import close_db
from datetime import datetime
from database import get_db

# Import blueprints
from routes.auth_routes import auth_bp
from routes.project_routes import project_bp
from routes.task_routes import task_bp

def create_app():
    """Create and configure the Flask application"""
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # ✅ IMPORTANT: Set secret key for sessions
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    
    # Enable CORS for frontend (React/Vue/etc running on different port)
    # This allows your API to be called from a different domain
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5500"])
    
    # Register blueprints with their URL prefixes
    app.register_blueprint(auth_bp)      # All auth routes will be under /api/auth
    app.register_blueprint(project_bp)    # All project routes will be under /api/projects
    app.register_blueprint(task_bp)       # All task routes will be under /api/tasks
    
    # Ensure database connections are closed after each request
    app.teardown_appcontext(close_db)
    
    # Root route - simple welcome message
    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to Community TaskForce API",
            "version": "1.0.0",
            "endpoints": {
                "auth": {
                    "register": "POST /api/auth/register",
                    "login": "POST /api/auth/login",
                    "me": "GET /api/auth/me"
                },
                "projects": {
                    "all": "GET /api/projects",
                    "one": "GET /api/projects/<id>",
                    "create": "POST /api/projects",
                    "update": "PUT /api/projects/<id>",
                    "delete": "DELETE /api/projects/<id>"
                },
                "tasks": {
                    "by_project": "GET /api/projects/<id>/tasks",
                    "my_tasks": "GET /api/tasks/assigned",
                    "create": "POST /api/projects/<id>/tasks",
                    "update": "PUT /api/tasks/<id>",
                    "complete": "PUT /api/tasks/<id>/complete",
                    "delete": "DELETE /api/tasks/<id>"
                }
            }
        })
    
    # Health check endpoint (useful for monitoring if API is running)
    @app.route('/health')
    def health():
        """Health check endpoint"""
        
        database_status = "disconnected"
        
        try:
            # Try to get database connection
            db = get_db()
            
            if db is not None:
                # Try to execute a simple query
                cursor = db.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                
                if result:
                    database_status = "connected"
                else:
                    database_status = "degraded"
            else:
                database_status = "no_connection"
                
        except Exception as e:
            database_status = f"error: {str(e)}"
        
        # Build response
        response = {
            "service": "Community TaskForce API",
            "version": "1.0.0",
            "database": database_status,
            "timestamp": str(datetime.now()),
            "config": {
                "host": Config.MYSQL_HOST,
                "database": Config.MYSQL_DB,
                "user": Config.MYSQL_USER
            }
        }
        
        return jsonify(response), 200
    
    # Error handler for 404 - Route not found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found",
            "message": "Check the URL and try again"
        }), 404
    
    # Error handler for 500 - Internal server error
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "message": "Something went wrong on our end"
        }), 500
    
# Add this before "return app" in create_app()
    @app.route('/debug-routes')
    def debug_routes():
        """List all registered routes"""
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'url': str(rule)
            })
        return jsonify(routes)
    return app

# Create the app instance
app = create_app()

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # debug=True - Auto-restart on code changes

    # host='0.0.0.0' - Allow connections from other devices on network

    # port=5000 - Default Flask port