#This code reads secret information from your .env file so your app can use it.

import os #gives Python the ability to read environment variables (settings from outside the code)
from dotenv import load_dotenv #imports a function that can read your .env file

# Load variables from .env file
load_dotenv()

class Config:
    # Database connection settings
                    #Dictionary style
    # #The Pattern: os.getenv('VARIABLE_NAME', 'default_value')
    # 'host': os.getenv('DB_HOST'), #Database server address
    # 'user': os.getenv('DB_USER'), #Database username
    # 'password': os.getenv('DB_PASSWORD'), #Database password
    # 'database': os.getenv('DB_NAME') #Which database to use
                   #OR
    #Direct Class Variables
    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
    MYSQL_DB = os.getenv('DB_NAME', 'community_taskforce')

    #DEBUG PRINTS
    print("="*50)
    print("🔍 Config Loading Debug:")
    print(f"DB_HOST: {MYSQL_HOST}")
    print(f"DB_USER: {MYSQL_USER}")
    print(f"DB_PASSWORD: {'*' * len(MYSQL_PASSWORD) if MYSQL_PASSWORD else 'EMPTY'}")
    print(f"DB_NAME: {MYSQL_DB}")
    print("="*50)
    
    # App settings
    SECRET_KEY = os.getenv('SECRET_KEY') #Security key for sessions
    DEBUG = os.getenv('DEBUG', 'False') == 'True' #Debug mode on/off
    
    # Pagination
    ITEMS_PER_PAGE = 20 #How many items per page
