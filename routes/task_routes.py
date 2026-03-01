#TASK MANAGEMENT
# routes/task_routes.py
from flask import Blueprint, request, jsonify, session
from models.task import Task
from models.project import Project
from auth_helpers import login_required
from datetime import datetime

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@task_bp.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get all tasks for a specific project"""
    #check if project exists
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"Error": "Project not found"}), 404
    
    #optional status filter
    status = request.args.get('status')
    #Get tasks from database
    tasks = Task.get_by_project(project_id,status)
    #return tasks
    return jsonify(tasks), 200

@task_bp.route('/assigned', methods=['GET'])
@login_required #our custom decorator that: # Checks if user is logged in
# If not, returns 401 Unauthorized
# If yes, allows the function to run
def get_my_tasks():
    """Get all tasks assigned to the currently logged-in user"""
    user_id = session.get('user_id')
    #Get tasks assigned to this user
    tasks = Task.get_assigned_to_user(user_id)

    return jsonify(tasks)

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    task = Task.get_by_id(task_id)
    if task:
        return jsonify(task)
    return jsonify({"Error": "Task not found"}), 404

@task_bp.route('/project/<int:project_id>', methods=['POST'])
def create_task(project_id):
    """Create a new task in a project"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"Error": "Project not found"}), 404
    
    #get JSON body
    data = request.get_json()
    
    #validate required fields
    if not data:
        return jsonify({"Error": "No data provided"}), 404
    if not data.get('title'):
        return jsonify({"Error": "Title is required"}), 400 # Bad Request - client sent invalid data
    
    #get logged_in user"s id
    user_id = session.get('user_id')

    task = Task.create(
        project_id=project_id,
        title=data['title'],
        created_by= user_id,
        description=data.get('description'),
        assigned_to=data.get('assigned_to'),
        priority=data.get('priority','medium'), 
        due_date=data.get('due_date') #optional
    )

    if task:
        return jsonify(task), 201
    return jsonify({"Error": "Could not create task"}), 404

@task_bp.route('/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """Mark task as completed"""
    #check if task exists
    task = Task.get_by_id(task_id)
    if not task:
        return jsonify({"Error": "Task not found"})
    #mark as complete
    completed_task = Task.mark_completed(task_id)
    if completed_task:
        return jsonify({
            "message": "Task marked as completed",
            "task" : completed_task
        })
    return jsonify({"Error": "Could not complete task"}), 400






