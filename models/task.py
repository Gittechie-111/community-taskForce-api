#TASKS WITH ASSIGNMENTS
from database import get_db
from mysql.connector import Error
from datetime import datetime #helps us track when things happen (completed_at timestamps).

@staticmethod
def create(project_id, title, created_by, description=None, assigned_to=None, 
           priority='medium', due_date=None):
    db = get_db()
    if not db:
        return None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO tasks (project_id, title, description, assigned_to, created_by, priority, due_date)" \
        "VALUES(%s, %s, %s, %s, %s, %s, %s)", (project_id, title, description, assigned_to, created_by, priority, due_date))
        db.commit()
        task = cursor.lastrowid
        cursor.close()
        return task
    except Error as e:
        print(f"Error in creating task: {e}")
        db.rollback()
        return None
    
@staticmethod
def get_by_id(task_id):
    #Get task by id
    db = get_db()
    if not db:
        return None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute ("""SELECT t.*,u_assign.username as assigned_to_name, u_create.username as created_by_name,
                        p.title as project_title  FROM tasks t LEFT JOIN u_assign ON t.assigned_to = u_assign.id, 
                        LEFT JOIN u_create ON t.created_by = u_create.id WHERE t.id=%s", (task_id,)""")
        #What it does: Get ALL columns from the tasks table (using t as its nickname)
        #Renaming columns to avoid conflicts
        #Get the username of the person this task is ASSIGNED TO 
        #Get the username of the person who CREATED this task
        #Get the title of the PROJECT this task belongs to
        #Find the user whose ID matches this task's assigned_to
        #Find the user whose ID matches this task's created_by
        #Only get the task with this specific ID
        task = cursor.fetchone()
        cursor.close()
        return task
    except Error as e:
        print(f"Error in getting task: {e}")
        db.rollback()
        return None
@staticmethod
def get_by_project(project_id, status=None):
    #Get all tasks for a project
    db = get_db()
    if not db:
        return []

    try:
        cursor = db.cursor(dictionary=True)
        query = """SELECT t.*. u_assign.username as assigned_to_name," 
        "FROM tasks t LEFT JOIN u_assign ON t.assigned_to = u_assign.id WHERE t.project_id=%s""" 
        #WHERE t.project_id=%s => this finds all rows where project_id=%s
        #A conditional query builder that changes SQL based on whether you want to filter by status or not
        params = [project_id] #filtering by project ID
        if status: 
            #If status is set execute this query
            query += "AND t.status=%s"
            params.append(status,)

        query += "ORDER BY t.priority DESC, t.due_date ASC"
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    except Error as e:
        print(f"Error in getting project tasks : {e}")
        db.rollback()
        return []
@staticmethod
def get_assigned_to_user(user_id):
    #Get tasks assigned to a specific user
    db = get_db()
    if not db:
        return None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT t.*, p.title as project_title FROM tasks t JOIN projects p ON t.project_id = p.id" \
        "WHERE t.assigned_to=%s AND t.status != 'completed ORDER BY t.priority DESC, t.due_date ASC", (user_id)) #Both conditions have to be true for a task to be returned
        #Why get project title? So when showing tasks to a user, they know which project each task belongs to
        #Only get tasks that HAVE a valid project
        #Only get tasks assigned to THIS specific user
        #Only get tasks that are NOT completed
        #Order by highest priority first, earliest deadline first
        #This query is like asking the database:"Show me all the tasks that belong to ME (user_id), that I HAVEN'T FINISHED yet, and also tell me which PROJECT each task is for. 
        #Oh, and please put the most URGENT tasks first, and if they have the same urgency, show the ones with the SOONEST DEADLINES first."
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    except Error as e:
        print(f"Error getting assigned tasks: {e}")
        db.rollback()
        return []

@staticmethod
def update(task_id, data):
    #Update task
    db = get_db()
    if not db:
        return None
    
    try:
        cursor = db.cursor()
        updates = []
        values = []
        allowed_fields = ['title', 'description', 'assigned_to', 'priority', 
                            'status', 'due_date']
        # Special handling for completed status
        #Automatically records the current time when someone marks a task as completed!
        if data.get('status') == 'completed' and 'completed_at' not in data:
            data['completed_at'] = datetime.now()
            allowed_fields.append('completed_at')
        
        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])
        
        if not updates:
            return Task.get_by_id(task_id)
        
        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        
        return Task.get_by_id(task_id)
            
    except Error as e:
        print(f"Error updating task: {e}")
        db.rollback()
        return None

@staticmethod
def delete(task_id):
    """Delete task"""
    db = get_db()
    if not db:
        return False
        
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    except Error as e:
        print(f"Error deleting task: {e}")
        db.rollback()
        return False

@staticmethod
def assign_task(task_id, user_id):
    """Assign task to user"""
    return Task.update(task_id, {'assigned_to': user_id})

@staticmethod
def mark_completed(task_id):
    """Mark task as completed"""
    return Task.update(task_id, {
        'status': 'completed',
        'completed_at': datetime.now()
    })

@staticmethod
def get_project_progress(project_id):
    """Get progress statistics for a project"""
    db = get_db()
    if not db:
        return None
        
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_tasks,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN priority = 'urgent' THEN 1 ELSE 0 END) as urgent_tasks
            FROM tasks
            WHERE project_id = %s
        """, (project_id,))
        
        stats = cursor.fetchone()
        cursor.close()
        
        if stats['total_tasks'] > 0:
            stats['completion_percentage'] = (stats['completed'] / stats['total_tasks']) * 100
        else:
            stats['completion_percentage'] = 0
            
        return stats
        
    except Error as e:
        print(f"Error getting project progress: {e}")
        return None
    