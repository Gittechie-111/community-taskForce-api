#USERS/VOUNTEERS
from database import get_db #gets databse connection
from mysql.connector import Error #catches database errors
import bcrypt #for password hashing
#Why bcrypt? Never store real passwords! If someone hacks your database, they only see scrambled versions.

class User:
#1) CREATING/ADDING NEW USERS
    @staticmethod
    def create(username, email, password, full_name=None, phone=None, is_admin=False):
        #Get database connection
        db = get_db()
        if not db:
            return None
        try:
            #Start the cursor
            cursor = db.cursor(dictionary=True)
            #Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            #Insert values into database
            cursor.execute("""INSERT INTO users  (username, email, password_hash, full_name, phone, is_admin)
                           VALUES(%s, %s, %s, %s, %s, %s)""",  (username, email, password_hash, full_name, phone, is_admin))
            #Save and get ID
            db.commit()
            user_id = cursor.lastrowid
            #Close cursor
            cursor.close()
            #Return new user
            return User.get_by_id(user_id)
        except Error as e:
            print(f"Error in create: {e}")
            db.rollback()
            return None

#2) FIND ONE USER
    @staticmethod
    def get_by_id(user_id):
    #Get database connection
        db = get_db()
        if not db:
            return None
        try:
            #Start the cursor
            cursor = db.cursor(dictionary=True)
            #Select every column except password from database(Don't select password_hash! Never send passwords to the frontend.)
            cursor.execute("SELECT id, username, email, full_name, phone, is_admin, created_at FROM users WHERE id=%s", (user_id,))
            #Fetch the user
            user = cursor.fetchone()
            #Close cursor
            cursor.close()
            #Return user
            return user
        except Error as e:
            print(f"Error in get_by_id: {e}")
            db.rollback()
            return None

    #3) FIND USER BY EMAIL
    @staticmethod
    def get_by_email(email):
        #Get database connection
        db = get_db()
        if not db:
            return None
        try:
            #Start the cursor
            cursor = db.cursor(dictionary=True)
            #Select every column from database
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            #Fetch the user
            user = cursor.fetchone()
            #Close cursor
            cursor.close()
            #Return user
            return user
        except Error as e:
            print(f"Error in get_by_email: {e}")
            db.rollback()
            return None

    #3) VERIFY PASSWORD
    @staticmethod
    def verify_password(email, password):
        #Find user by email
        user = User.get_by_email(email)
        #Check password(takes the password a user typed and compares it with the stored hash)
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            #Remove hashing before sending
            del user['password_hash']
            #Return user
            return user
        return None

    #4) UPDATING USER
    @staticmethod
    def update(user_id, data):
        #Get database connection
        db = get_db()
        if not db:
            return None

        #Start cursor
        try:
            cursor = db.cursor()
            updates = []
            values = []
            #Update only allowed fields
            allowed_fields = ['full_name', 'phone']
            for field in allowed_fields:
                if field in data:
                    updates.append(f"{field} =%s")
                    values.append(data[field])
            #If no updates return current user
            if not updates:
                return User.get_by_id(user_id)
            #Append user_id to values
            values.append(user_id)
            #Set query and execute it
            query = (f"UPDATE users SET {', '.join(updates)} WHERE id=%s")
            cursor.execute(query, values)
            #Commit and close db
            db.commit()
            cursor.close()
        except Error as e:
            print(f"Error in update: {e}")
            db.rollback()
            return None
