# models/__init__.py
# What is a Base Class?

# Think of it like a parent who teaches their children basic skills:

#     Parent (BaseModel) knows how to: find things by ID, get all records

#     Children (User, Project, Task) inherit these skills automatically
from database import get_db
from mysql.connector import Error

class BaseModel: #a blueprint class other models will inherit from
    """Base class with common database methods"""
    
    @staticmethod
    def _dict_to_model(cursor, row): #FORMATTER
        """Convert database row to dictionary"""
        if not row:
            return None
        columns = [col[0] for col in cursor.description] #Tells us the column names (like "id", "name", "email") and makes a list of those names
        return dict(zip(columns, row)) # Pairs each name with its value. dict() turns pairs into dictionaries
    
    @classmethod
    def find_by_id(cls, table, id_value):
        """Find record by ID number from any table.
        cls is a reference to the class itself
        What cls gives you access to:

        Other class methods - Can call other @classmethod or @staticmethod methods

        Class variables - Variables shared by all instances

        The class name - Useful for inheritance!
        table = Which table to look in (users, projects, tasks)
        id_value = The ID number to find
        """
        db = get_db()
        if not db:
            return None
        
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table} WHERE id = %s", (id_value,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error finding {table} by id: {e}")
            return None
    
    @classmethod
    def find_all(cls, table, order_by='id DESC'):
        """Find all records from any table, newest first"""
        db = get_db()
        if not db:
            return []
        
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table} ORDER BY {order_by}")
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error finding all {table}: {e}")
            return []
        
#Example Usage:
# Get all users
# users = BaseModel.find_all("users")

# Get all projects, sorted by title
# projects = BaseModel.find_all("projects", "title ASC")