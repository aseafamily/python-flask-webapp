from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from db import db_uri
from datetime import datetime, timedelta
import pytz

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
    start_of_week = get_client_time(start_of_week)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_client_time(date):
    # Ensure the input date is timezone-aware
    if date.tzinfo is None:
        # If the date is naive (no timezone info), assume it's UTC
        date = pytz.utc.localize(date)
    # Define Seattle's timezone
    seattle_timezone = pytz.timezone('America/Los_Angeles')
    # Convert the date to Seattle's timezone
    seattle_time = date.astimezone(seattle_timezone)
    return seattle_time

