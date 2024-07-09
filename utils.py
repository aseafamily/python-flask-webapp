from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from db import db_uri
from datetime import datetime, timedelta
import pytz
import re

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
    # start_of_week = get_client_time(start_of_week)
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

# Function to convert 'None' string to Python None
def convert_none_string_to_none(value):
    if value == 'None':
        return None
    return value

def get_match_round_abbreviation(match):
    special_rounds = {
        "Quarterfinals": "QF",
        "Semifinals": "SF",
        "Finals": "F"
    }

    round_name = match.match_round
    
    for key, value in special_rounds.items():
        if key in round_name:
            round_name = round_name.replace(key, value)

    if match.match_draw != 'Main':
        if not round_name:
            if any(char.isdigit() for char in match.match_draw):
                digits = ''.join(filter(str.isdigit, match.match_draw))
                round_name = match.match_draw[0] + digits
            else:
                round_name = match.match_draw

        elif not any(char.isdigit() for char in match.match_draw) and '-' not in round_name:
            round_name = f"{match.match_draw[0]}-{round_name}"

    return round_name.upper()

def generate_title(location_name, ignore_digits=True):
    # Remove any non-alphabetic characters and convert to uppercase
    location_name = re.sub('[^A-Za-z ]', '', location_name).upper()

    # Check if location_name is already an acronym (less than four uppercase characters)
    if len(location_name) <= 4 and location_name.isupper():
        return location_name
    
    # Split the location name into words
    words = location_name.split()

    # Initialize acronym
    acronym = ""

    # Build acronym from first letters of each word (up to 4 characters)
    for word in words:
        if not (ignore_digits and word.isdigit()):  # Skip words that are numbers if ignore_digits is True
            acronym += word[0].upper()

            # Break loop if acronym length reaches 4 characters
            if len(acronym) >= 4:
                break

    return acronym