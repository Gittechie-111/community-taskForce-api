#DB CONNECTION
#Print statements are for debugging
import mysql.connector
from flask import g
from config import Config

def get_db():
    if 'db' not in g:
        try:
            print("🆕 Creating a new database connection")
            g.db = mysql.connector.connect(
                host=Config.MYSQL_HOST,        # ← Expects MYSQL_HOST
                user=Config.MYSQL_USER,        # ← Expects MYSQL_USER
                password=Config.MYSQL_PASSWORD, # ← Expects MYSQL_PASSWORD
                database=Config.MYSQL_DB  
            )
            print("✅ Database connection successful")

        except mysql.connector.Error as e:
            print(f"❌ Connection failed: {e}")
            return None
    else:
        print("🔄 Reusing existing database connection")
    return g.db
    
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print("🔒 Closing database connection")
        db.close()

