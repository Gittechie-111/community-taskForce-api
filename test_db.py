# test_db.py
import mysql.connector
from config import Config

print(f"Testing connection with:")
print(f"Host: {Config.MYSQL_HOST}")
print(f"User: {Config.MYSQL_USER}")
print(f"Database: {Config.MYSQL_DB}")
print(f"Password: {'*' * len(Config.MYSQL_PASSWORD)}")

try:
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    print("✅ Connection successful!")
    conn.close()
except mysql.connector.Error as e:
    print(f"❌ Connection failed: {e}")
