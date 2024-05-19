from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Get the database credentials from environment variables
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

if username and password:
    print("Database credentials loaded successfully.")
else:
    print("Failed to load database credentials.")


db = SQLAlchemy()

db_uri = f'mssql+pyodbc://{username}:{password}@bhmtest.database.windows.net/myTest?driver=ODBC+Driver+17+for+SQL+Server&connect_timeout=30'