# COMMUNITY PROJECTS
# 🔑 Key Takeaways

#     JOINs connect related data (projects + users)

#     Aggregates (COUNT, SUM) calculate stats automatically

#     Completion percentage is calculated in Python, not SQL

#     CASCADE delete keeps database clean

#     Status filtering lets you organize projects

# This model turns raw database rows into meaningful project data with progress stats! 🚀
from database import get_db
from mysql.connector import Error
class Project:
    @staticmethod
    def create(title, description, created_by, location=None, start_date=None, end_date=None):
        db = get_db()
        if not db:
            return None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("INSERT VALUES INTO projects (title, description, location, start_date, end_date, created_by) VALUES(%s, %s, %s, %s, %s, %s)", (title, description, location, start_date, end_date, created_by))
            db.commit()
            project_id = cursor.lastrowid
            cursor.close()
            return Project.get_by_id(project_id)
        except Error as e:
            print(f"Error in creating project: {e}")
            db.rollback()
            return None
        
    @staticmethod
    def get_by_id(project_id):
        db = get_db()
        if not db:
            return None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT p.*, u.username as creator_name FROM " \
            "projects p LEFT JOIN users u ON p.created_by = u.id WHERE id=%s", (project_id,))
        # p.* = All columns from projects table
        # u.username as creator_name = Get the creator's username from users table
        # LEFT JOIN = Connect projects to users based on created_by = users.id
        # Result: Project info + the name of who created it!
            project = cursor.lastrowid
            cursor.close()
            return project
        except Error as e:
            print(f"Error in getting project: {e}")
            return None
    @staticmethod
    def get_all(status=None):
        """Get all projects, optionally filtered by status"""
        db = get_db()
        if not db:
            return None
        try:
            cursor = db.cursor(dictionary=True)
            query ="""SELECT p.*, u.username as creator_name, COUNT(t.id) as total_tasks,
            SUM(CASE WHEN t.status='completed' THEN 1 ELSE 0 END) as completed_tasks
            FROM projects p 
            LEFT JOIN users u ON p.created_by = u.id
            LEFT JOIN tasks ON p.id = t.project_id"""
            #A conditional query builder that changes SQL based on whether you want to filter by status or not
            if status:
                #if status is set, execute this query
                query += "WHERE p.status=%s"
                params = (status,)
                #The params tuple provides the values for the %s placeholders:
            else:
                params =()
            #Group and order
            query += "GROUP BY P.id ORDER BY created_at DESC" #combines all tasks for each product into one row and shows the newest first
            cursor.execute(query, params)
            projects = cursor.fetchall()
            #Calculate percentage completion
            for project in projects:
                if project['total_tasks'] > 0:
                    project['completion_percentage'] = project['completed_tasks'] / project['total_tasks'] *100
                else:
                    project['completed_percentage'] = 0
                return projects
        except Error as e:
            print(f"Error in getting all projects: {e}")
            return []
        
    @staticmethod
    def update(project_id, data):
        db = get_db()
        if not db:
            return None
        try:
            cursor = db.cursor()
            updates = []
            values = []

            allowed_fields = ['title', 'description', 'location', 'start_date', 'end_date', 'status']
            for field in allowed_fields:
                if field in data:
                    updates.append(f"{field} =%s")
                    values.append(data[field])
            if not updates:
                return Project.get_by_id(project_id)
            values.append(project_id)
            query = (f"UPDATE projects SET {', '.join(updates)} WHERE id=%s")
            cursor.execute(query, values)
            db.commit()
            cursor.close()
        except Error as e:
            print(f"Error in updating projects: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete(project_id):
        db = get_db()
        if not db:
            return None
        try:
            cursor = db.cursor(dicionary=True)
            cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
            affected = cursor.rowcount #No of rows deleted
            db.commit()
            cursor.close()
            return affected > 0 #return true if something is deleted
        except Error as e:
            print(f"Error in deleting project: {e}")
            db.rollback()
            return None

