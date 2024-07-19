from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db, db_uri
from tennis import get_or_create_player, generate_match_summary
from datetime import datetime, timedelta
from db_tennis import Tennis
from db_match import Match
from cmd_match_score import parse_match_string

def get_integer_from_form(key: str) -> int:
    if key in match_info:
        try:
            return int(match_info[key])
        except ValueError:
            pass
    return None

def get_integer_from_form100(key):
    try:
        value = None
        if key in match_info:
            value = match_info[key]
        
        # Check if value is available
        if value is not None:
            # Cast value to float and multiply by 100
            value_as_float = float(value)
            result = int(value_as_float * 100)
            return result
        
        # If the value is not found, return None or handle accordingly
        return None

    except (ValueError, TypeError):
        # Handle the case where the value cannot be converted to float
        return None

# Forest Crest Athletic Club
# Mountlake Terrace
# Harbor Square Athletic Club
# Edmonds
class Club:
    def __init__(self, name, city, state):
        self.name = name
        self.city = city
        self.state = state

# Initialize club objects
clubs = {
    'am': Club('Amy Yee Indoor Tennis Center', 'Seattle', 'WA'),
    'bc': Club('Bellevue Club', 'Bellevue', 'WA'),
    'cp': Club('Central Park Tennis Club', 'Kirkland', 'WA'),
    'etc': Club('Eastside Tennis Center', 'Kirkland', 'WA'),
    'fc': Club('Forest Crest Athletic Club', 'Mountlake Terrace', 'WA'),
    'hs': Club('Harbor Square Athletic Club', 'Edmonds', 'WA'),    
    'mi': Club('Mercer Island Country Club', 'Mercer Island', 'WA'),    
    'ntc': Club('Nordstrom Tennis Center', 'Seattle', 'WA'),
    'pl': Club('Pine Lake Columbia Athletic Clubs', 'Sammamish', 'WA'),
    'rb': Club('Robinswood Tennis Center', 'Bellevue', 'WA'),
    'sl': Club('Silver Lake Columbia Athletic Club', 'Everett', 'WA'),
    'sp': Club('Tennis Center Sand Point', 'Seattle', 'WA'),
    'ttc': Club('Tualatin Hills Tennis Stadium', 'Beaverton', 'OR'),
    'vtc': Club('Vancouver Tennis Center', 'Vancouver', 'WA')
}
###################
# Input for every match
player1_id = 0
team1_serve = True


use_googleKeep = True

##### The following need change
is_singles = False
date_input = "2020-01-09"
duration = ""
is_indoor=True
club_key = "pl"
location = clubs[club_key].name
match_city=clubs[club_key].city
match_state=clubs[club_key].state
 
#location = "The Valley Athletic Club"
#match_city="Tumwater"
#match_state="WA"

match_name = "2020 Adult 40 & Over - 3.0 Men"
match_level="USTA 3.0"
match_link="https://tennislink.usta.com/leagues/Main/StatsAndStandings.aspx?t=0&par1=2010809878#&&s=7%7c%7c0%7c%7c1007658036%7c%7c2020"
match_event="Adults 40+"
match_draw="Doubles 3"
match_round="Season"
comments='''
ETC-RazorBacks-Che vs PL-Rangaswami
D3, 5-0 
'''
scores=''

match_string = """
(2.73, UTR4.47) (A)
/Shu Shen (2.93, UTR5)
7-5; 6-4
David Presba (2.65, UTR4)
/Gregory Snow (2.86, UTR4)
"""
rank_types = ["usta", "utr"]
###################



###################

team1_won, match_info = parse_match_string(match_string, rank_types)

# Player info
player2 = match_info["player2"]
player3 = ""
player4 = ""

if not is_singles:
    player3 = match_info["player3"]
    player4 = match_info["player4"]

# Tennis table
category = "Match"
details = ""

# start
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,  # Adjust as needed
    'pool_recycle': 3600,  # Optional: Recycle connections after 1 hour
    'pool_timeout': 30,  # Optional: Maximum time to wait for a connection from the pool
}

db = SQLAlchemy(app)

# Push the application context
with app.app_context():
    # Create the tables in the database (if they don't exist)
    db.create_all()

    player2_id = get_or_create_player(player2, db.session, None)
    player3_id = -1
    player4_id = -1

    if not is_singles:
        player3_id = get_or_create_player(player3, db.session, None)
        player4_id = get_or_create_player(player4, db.session, None)

    date = datetime.strptime(date_input, '%Y-%m-%d')
    tennis_instance = Tennis(
        date=date,
        duration=duration,
        location=location,
        category=category,
        details=details,
        player=player1_id
    )

    db.session.add(tennis_instance)
    db.session.flush()

    print(tennis_instance.id)

    # Add a new match using the player1_id
    new_match = Match(
        duration=duration,
        location=location,
        date=date,
        type='S' if is_singles else 'D',
        player1=player1_id,
        player2=player2_id,
        player3=None if is_singles else player3_id,
        player4=None if is_singles else player4_id,
        team1_set1=get_integer_from_form('team1_set1'),
        team1_set1_tb=get_integer_from_form('team1_set1_tb'),
        team2_set1=get_integer_from_form('team2_set1'),
        team2_set1_tb=get_integer_from_form('team2_set1_tb'),
        team1_set2=get_integer_from_form('team1_set2'),
        team1_set2_tb=get_integer_from_form('team1_set2_tb'),
        team2_set2=get_integer_from_form('team2_set2'),
        team2_set2_tb=get_integer_from_form('team2_set2_tb'),
        team1_set3=get_integer_from_form('team1_set3'),
        team1_set3_tb=get_integer_from_form('team1_set3_tb'),
        team2_set3=get_integer_from_form('team2_set3'),
        team2_set3_tb=get_integer_from_form('team2_set3_tb'),
        team1_won=team1_won,
        team1_serve=True,
        match_name=match_name,
        match_level=match_level,
        match_link=match_link,
        match_event=match_event,
        match_draw=match_draw,
        match_round=match_round,
        match_city=match_city,
        match_state=match_state,
        is_indoor=is_indoor,
        comments=comments,
        scores=scores,
        tennis_id=tennis_instance.id,
        player1_wtn = get_integer_from_form100('player1_wtn'),
        player1_utr = get_integer_from_form100('player1_utr'),
        player1_usta = get_integer_from_form100('player1_usta'),
        player1_seed = get_integer_from_form('player1_seed'),
        player2_wtn = get_integer_from_form100('player2_wtn'),
        player2_utr = get_integer_from_form100('player2_utr'),
        player2_usta = get_integer_from_form100('player2_usta'),
        player2_seed = get_integer_from_form('player2_seed'),
        player3_wtn = get_integer_from_form100('player3_wtn'),
        player3_utr = get_integer_from_form100('player3_utr'),
        player3_usta = get_integer_from_form100('player3_usta'),
        player3_seed = get_integer_from_form('player3_seed'),
        player4_wtn = get_integer_from_form100('player4_wtn'),
        player4_utr = get_integer_from_form100('player4_utr'),
        player4_usta = get_integer_from_form100('player4_usta'),
        player4_seed = get_integer_from_form('player4_seed')
    )
    db.session.add(new_match)
    tennis_instance.details = generate_match_summary(new_match, player2, player3, player4)
    db.session.commit()

    print(f"New match created {new_match.id}: {tennis_instance.details}")




