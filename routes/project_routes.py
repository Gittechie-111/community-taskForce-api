#PROJECT MANAGEMENT
#These are the endpoints your frontend will need so users can create and view projects
from flask import Blueprint, request, jsonify, session
from models.project import Project
from models.user import User #FOR AUTHENTICATION
from auth_helpers import login_required  # ← Import our decorator!

#Create blueprint
project_bp = Blueprint('projects', __name__, url_prefix='/api/projects')
#GET ALL PROJECTS (with optional status filter)
@project_bp.route('/', methods=['GET'])
def get_projects():
    # Get status from query string: /api/projects?status=active
    status = request.args.get('status')
    #call model method and Gets all projects, filtered by status if provided
    projects = Project.get_all(status)
    return jsonify(projects), 200
#Example requests:
# Get ALL projects
# GET /api/projects/

# # Get ONLY active projects
# GET /api/projects/?status=active

# # Get ONLY completed projects
# GET /api/projects/?status=completed

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    # Get project from database
    project = Project.get_by_id(project_id)
    if project:
        return jsonify(project), 200
    return jsonify({"Error": "Project not found"}), 404

@project_bp.route('/', methods=['POST'])
@login_required  # ← THIS IS IT! Protects the route
def create_project():
    #read json body
    data = request.get_json()
    #validate required fields
    if not data:
        return jsonify({"Error": "Data not provided"}), 400
    if not data.get('title'):
        return jsonify({"Error": "Project title is required"}), 400
    if not data.get('description'):
        return jsonify({"Error": "Project description is required"}), 400
    
    # ✅ Get the REAL logged-in user ID from session!
    # The decorator already checked they're logged in
    created_by = session.get('user_id')
    
    #calling model to insert into database
    project = Project.create(
        title=data['title'],
        description=data['description'],
        created_by=created_by,
        location=data.get('location'),        # Optional
        start_date=data.get('start_date'),    # Optional
        end_date=data.get('end_date')          # Optional
    )
    
    if project:
        return jsonify(project)
    return jsonify({"Error": "Could not create project"}), 400

@project_bp.route('/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    data = request.get_json()
    if not data:
        return jsonify({"Error": "No data provided"}), 400
    
     # Optional: Check if user owns this project
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    # Check if user is creator or admin
    current_user_id = session.get('user_id')
    if project['created_by'] != current_user_id:
        # Allow admins to edit any project
        user = User.get_by_id(current_user_id)
        if not user or not user.get('is_admin'):
            return jsonify({"error": "You don't have permission to edit this project"}), 403
        
    updated = Project.update(project_id, data)

    if updated:
        return jsonify(updated)
    return jsonify({"Error": "Could not update project"}), 404

@project_bp.route('/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    # Optional: Check if user owns this project
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    # Check if user is creator or admin
    current_user_id = session.get('user_id')
    if project['created_by'] != current_user_id:
        user = User.get_by_id(current_user_id)
        if not user or not user.get('is_admin'):
            return jsonify({"error": "You don't have permission to delete this project"}), 403

    success = Project.delete(project_id)
    if success:
        return jsonify({"Message": "Project deleted successfully", "project_id" : project_id}), 200
    else:
        return jsonify({"Error": "Project not found"}), 404






