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

def generate_level(level_name):
    # Check if the level_name is a string
    level_name = str(level_name)

    # Remove leading and trailing spaces
    level_name = level_name.strip()

    # Handle "Level X" and "Level X Open" formats
    match = re.match(r'Level (\d)( Open)?', level_name, re.IGNORECASE)
    if match:
        level = match.group(1)
        open_suffix = match.group(2)
        return f"L{level}" + ("O" if open_suffix else "")

    # Handle "USTA X.X" format
    match = re.match(r'USTA (\d\.\d)', level_name, re.IGNORECASE)
    if match:
        return match.group(1)

    # If no pattern matched, return the original string as-is
    return generate_title(level_name)

def generate_title(location_name, ignore_digits=True, including_year=False):
    # Extract year if including_year is True
    year = ""
    if including_year:
        year_match = re.search(r'\b\d{4}\b', location_name)
        if year_match:
            year = year_match.group()
    
    # Remove any non-alphabetic characters and convert to uppercase
    location_name = re.sub('[^A-Za-z ]', '', location_name).upper()

    # Check if location_name is already an acronym (less than four uppercase characters)
    if len(location_name) <= 4 and location_name.isupper():
        return year + location_name if year else location_name
    
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

    return year + acronym if year else acronym

def extract_number_from_string(input_string):
    match = re.search(r'\d+', input_string)
    if match:
        number = match.group()
        if "+" in input_string:
            return f"{number}+"
        return f"U{number}"
    else:
        return generate_title(input_string, False)
    
def generate_match_summary(match, player2, player3, player4):
    # Extract player names
    player1_name = '' # get_brief_player_name(request.form['player1'])
    player2_name = get_brief_player_name(player2)
    if match.type == 'D':
        player3_name = get_brief_player_name(player3)
        player4_name = get_brief_player_name(player4)
        player1_name = f"/{player3_name} "
        player2_name = f"{player2_name}/{player4_name}"

    # Extract scores
    sets_summary = []
    for i in range(1, 4):  # Assuming matches have up to 3 sets
        team1_score = getattr(match, f"team1_set{i}")
        team2_score = getattr(match, f"team2_set{i}")
        team1_tb = getattr(match, f"team1_set{i}_tb", None)
        team2_tb = getattr(match, f"team2_set{i}_tb", None)

        if team1_score is not None and team2_score is not None:
            set_summary = f"{team1_score}"
            if team1_tb is not None:
                set_summary += f"({team1_tb})"
            set_summary += f"-{team2_score}"
            if team2_tb is not None:
                set_summary += f"({team2_tb})"
            sets_summary.append(set_summary)

    # Combine all details
    match_summary = f"{player1_name}"
    match_summary += ";".join(sets_summary)
    match_summary += f" {player2_name}"

    level = generate_level(match.match_level)
    title = generate_title(match.match_name, True)
    round = get_match_round_abbreviation(match)
    event = extract_number_from_string(match.match_event)

    match_summary += f" {title} {level} {event} {round}"

    return match_summary

def get_brief_player_name(player):
    # Split the full name into parts
    parts = player.split()

    # Construct the formatted name
    if len(parts) >= 2:
        formatted_name = f"{parts[0]}{parts[1][0].upper()}"
    else:
        formatted_name = player

    return formatted_name