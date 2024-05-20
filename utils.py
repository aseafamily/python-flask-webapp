from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from db import db_uri
from datetime import datetime, timedelta

# Hardcoded dictionary mapping user IDs to names
user_dict = {
    '1': 'Andrew',
    '2': 'Emily',
    '0': 'Alex'
}

# Retry decorator with exponential backoff
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), retry_error_callback=lambda x: isinstance(x, OperationalError))
def test_database_connection(uri):
    print("Test: Attempting to connect to the database...")
    engine = create_engine(uri)
    try:
        conn = engine.connect()
        conn.close()
        print("Test: Connection successful!")
        return True
    except OperationalError as e:
        print(f"Test: Connection attempt failed: {e}")
        raise e
    
def test_connection():
    try:
        if test_database_connection(db_uri):
            return "Connection successful!"
    except OperationalError:
        return "Connection failed."
    
def get_week_range(date):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week