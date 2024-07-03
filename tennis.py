from flask import Blueprint
from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort
from db import db
from db_serve import Serve, ServeAnalysis, ServeStatus
from db_tennis import Tennis, TennisAnalysis, TennisStatus
from db_match import Match
from db_player import Player
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy import cast, String, desc
from utils import test_connection, user_dict, get_week_range, get_client_time
from flask_login import login_required
import math
from sqlalchemy.orm import aliased
import re

tennis_bp = Blueprint('tennis', __name__)

@tennis_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Tennis.query.with_entities(func.cast(Tennis.category, String)).distinct().order_by(func.cast(Tennis.category, String)).all()
    categories_list = [category[0] for category in categories]
    return jsonify(categories_list)

@tennis_bp.route('/tennis', methods=['POST', 'GET'])
@login_required
def tennis_index():
    player_id = request.args.get('u')
    category_filter = request.args.get('category', '')

    if request.method == 'GET':
        # Initial query
        tennis_all_query = Tennis.query.filter_by(player=player_id)

        # Add category filter if it exists and is not empty
        if category_filter:
            tennis_all_query = tennis_all_query.filter_by(category=category_filter)

        # Order the results by date and id in descending order
        tennis_all_query = tennis_all_query.order_by(desc(Tennis.date), desc(Tennis.id))

        # Execute the query
        tennis_all = tennis_all_query.all()

        current_date = get_client_time(datetime.utcnow())

        weekly_results = db.session.query(func.extract('year', Tennis.date).label('year'),
                                                func.extract('week', Tennis.date).label('week'),
                                                func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .group_by(func.extract('year', Tennis.date), func.extract('week', Tennis.date)) \
                                    .all()

        # Initialize variables for weekly data
        total_duration_weekly = 0
        total_records_weekly = 0

        # Iterate over the weekly results and calculate totals
        for _, _, duration, records in weekly_results:
            total_duration_weekly += duration or 0
            total_records_weekly += records or 0

        # Calculate the number of weeks
        num_weeks = len(weekly_results)

        # Calculate averages for weekly data
        average_duration_per_week = total_duration_weekly / num_weeks if num_weeks > 0 else 0
        average_records_per_week = total_records_weekly / num_weeks if num_weeks > 0 else 0

        # Query to get total serves, total duration, and count of all records for the player
        total_results = Tennis.query.with_entities(func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .first()

        # Extract values from the total results
        total_duration = total_results[0] or 0
        total_records = total_results[1] or 0

        # Calculate the time since the first entry
        first_entry = Tennis.query.filter_by(player=player_id).order_by(Tennis.date.asc()).first()
        time_since_first_entry = datetime.now() - first_entry.date if first_entry else timedelta(0)

        # Calculate fitness total
        total_fitness_result = Tennis.query.with_entities(func.sum(Tennis.duration)) \
                                    .filter(Tennis.player == player_id) \
                                    .filter(cast(Tennis.category, String) == 'Fitness') \
                                    .first()
        
        total_fitness_duration = total_fitness_result[0] or 0

        # Calculate fitness weekly
        fitness_weekly_results = db.session.query(func.extract('year', Tennis.date).label('year'),
                                                func.extract('week', Tennis.date).label('week'),
                                                func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .filter(cast(Tennis.category, String) == 'Fitness') \
                                    .group_by(func.extract('year', Tennis.date), func.extract('week', Tennis.date)) \
                                    .all()
        
        # Initialize variables for weekly data
        total_fitness_duration_weekly = 0
        total_fitness_records_weekly = 0

        # Iterate over the weekly results and calculate totals
        for _, _, duration, records in fitness_weekly_results:
            total_fitness_duration_weekly += duration or 0
            total_fitness_records_weekly += records or 0

        # Calculate the number of weeks
        num_weeks = len(fitness_weekly_results)

        # Calculate averages for weekly data
        average_fitness_duration_per_week = total_fitness_duration_weekly / num_weeks if num_weeks > 0 else 0
        average_fitness_records_per_week = total_fitness_records_weekly / num_weeks if num_weeks > 0 else 0


        # Round up to days
        time_since_first_entry_rounded = timedelta(days=time_since_first_entry.days)

        # Create an instance of TennisAnalysis class
        tennis_analysis = TennisAnalysis()
        tennis_analysis.total_duration = total_duration
        tennis_analysis.total_records = total_records
        tennis_analysis.average_duration_per_week = average_duration_per_week
        tennis_analysis.average_records_per_week = average_records_per_week
        tennis_analysis.time_since_first_entry = time_since_first_entry_rounded
        tennis_analysis.total_fitness_duration = total_fitness_duration
        tennis_analysis.average_fitness_duration_per_week = average_fitness_duration_per_week

        return render_template('tennis.html', tennis_all=tennis_all, now=current_date, tennis_analysis=tennis_analysis)
    else:
        # Retrieve form data
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        duration = request.form['duration']
        location = request.form['location']
        category = request.form['category']
        details = request.form['details']
        player = player_id

        if category == 'Match':
            try:
                match_type = request.form['match_type']
                is_singles = match_type == 'singles'
                player1_id = get_or_create_player(request.form['player1'], db.session, request.form['player1_id'])
                player2_id = get_or_create_player(request.form['player2'], db.session, request.form['player2_id'])
                player3_id = -1
                player4_id = -1

                if not is_singles:
                    player3_id = get_or_create_player(request.form['player3'], db.session, request.form['player3_id'])
                    player4_id = get_or_create_player(request.form['player4'], db.session, request.form['player4_id'])

                tennis_instance = Tennis(
                    date=date,
                    duration=duration,
                    location=location,
                    category=category,
                    details=details,
                    player = player
                )

                # Add the instance to the database
                db.session.add(tennis_instance)
                db.session.flush()

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
                    team1_won=True if request.form['match_outcome'] == 'team1_won' else False,
                    match_name=request.form['match_name'],
                    match_level=request.form['match_level'],
                    match_link=request.form['match_link'],
                    match_event=request.form['match_event'],
                    match_draw=request.form['match_draw'],
                    match_round=request.form['match_round'],
                    match_city=request.form['match_city'],
                    match_state=request.form['match_state'],
                    is_indoor=True if request.form['court_type'] == 'indoor' else False,
                    comments=request.form['match_comments'],
                    tennis_id=tennis_instance.id
                )
                db.session.add(new_match)
                tennis_instance.details = generate_match_summary(new_match)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                # No need to close the session manually; Flask-SQLAlchemy handles this
                pass
        else:
            # Create an instance of Tennis class
            tennis_instance = Tennis(
                date=date,
                duration=duration,
                location=location,
                category=category,
                details=details,
                player = player
            )

            # Add the instance to the database
            db.session.add(tennis_instance)
            db.session.commit()

        redirect_url = f'/tennis?u={player_id}'
        if category_filter:
            redirect_url += f'&category={category_filter}'

        return redirect(redirect_url)
    
def get_or_create_player(full_name: str, session, player_id: str = '') -> int:
    if player_id:
        try:
            return int(player_id)
        except ValueError:
            raise ValueError("Invalid player_id provided. It must be a valid integer.")

    # Split the full name into first and last name
    name_parts = full_name.strip().split()
    if len(name_parts) == 1:
        first_name = name_parts[0]
        last_name = ''
    else:
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])  # Support for middle names and compound last names

    # Try to find the player in the database
    query = session.query(Player.id, Player.first_name, Player.last_name).filter(
        func.lower(Player.first_name) == func.lower(first_name),
        func.lower(Player.last_name) == func.lower(last_name)
    )
    existing_player = query.first()
    
    if existing_player:
        # Player found, return the player ID
        return existing_player.id
    else:
        # Player not found, create a new player
        new_player = Player(
            first_name=first_name,
            last_name=last_name,
            gender=None,           # Set default values for other fields if necessary
            birthday=None,
            year_graduation=None,
            utr_profile=None,
            usta_profile=None,
            usta_id=None,
            utr=None,
            wtn=None,
            usta=None,
            utr_date=None,
            wtn_date=None,
            usta_date=None
        )
        session.add(new_player)
        session.commit()  # Commit to get the new player ID
        
        return new_player.id
    
def get_integer_from_form(form_key: str) -> int:
    if form_key in request.form and request.form[form_key]:
        try:
            return int(request.form[form_key])
        except ValueError:
            pass
    return None
    
@tennis_bp.route('/tennis/delete/<int:id>')
@login_required
def tennis_delete(id):
    tennis_to_delete = Tennis.query.get_or_404(id)
    match_to_delete = Match.query.filter_by(tennis_id=tennis_to_delete.id).first()
    uid = request.args.get('u')

    try:
        db.session.delete(tennis_to_delete)
        if match_to_delete is not None:
            db.session.delete(match_to_delete)
        db.session.commit()

        redirect_url = f'/tennis?u={uid}'
        category_filter = request.args.get('category', '')
        if category_filter:
            redirect_url += f'&category={category_filter}'
        return redirect(redirect_url)
    except:
        return 'There was a problem deleting that task'

# Define a helper function to handle generating names
def generate_name(first_name, last_name):
    if first_name and not last_name:
        return first_name.strip()  # Return first_name if last_name is empty
    elif first_name and last_name:
        return (first_name + ' ' + last_name).strip()  # Concatenate both names
    else:
        return None  # Return None if both names are empty or None
        
@tennis_bp.route('/tennis/update/<int:id>', methods=['GET', 'POST'])
@login_required
def tennis_update(id):
    tennis = Tennis.query.get_or_404(id)
    match = None
    uid = request.args.get('u')

    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        duration = request.form['duration']
        location = request.form['location']

        tennis.date = date
        tennis.duration = duration
        tennis.location = location
        tennis.category = request.form['category']
        tennis.details = request.form['details']

        if tennis.category == 'Match':
            match_type = request.form['match_type']
            is_singles = match_type == 'singles'
            player1_id = get_or_create_player(request.form['player1'], db.session, request.form['player1_id'])
            player2_id = get_or_create_player(request.form['player2'], db.session, request.form['player2_id'])
            player3_id = -1
            player4_id = -1

            if not is_singles:
                player3_id = get_or_create_player(request.form['player3'], db.session, request.form['player3_id'])
                player4_id = get_or_create_player(request.form['player4'], db.session, request.form['player4_id'])

            match = Match.query.filter_by(tennis_id=tennis.id).first()
            if not match:
                # Create a new match
                match = Match(
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
                    team1_won=True if request.form['match_outcome'] == 'team1_won' else False,
                    match_name=request.form['match_name'],
                    match_level=request.form['match_level'],
                    match_link=request.form['match_link'],
                    match_event=request.form['match_event'],
                    match_draw=request.form['match_draw'],
                    match_round=request.form['match_round'],
                    match_city=request.form['match_city'],
                    match_state=request.form['match_state'],
                    is_indoor=True if request.form['court_type'] == 'indoor' else False,
                    comments=request.form['match_comments'],
                    tennis_id=tennis.id
                )
                db.session.add(match)
            else:
                # Update the match
                match.duration=duration
                match.date=date
                match.type='S' if is_singles else 'D'
                match.player1=player1_id
                match.player2=player2_id
                match.player3=None if is_singles else player3_id
                match.player4=None if is_singles else player4_id
                match.team1_set1=get_integer_from_form('team1_set1')
                match.team1_set1_tb=get_integer_from_form('team1_set1_tb')
                match.team2_set1=get_integer_from_form('team2_set1')
                match.team2_set1_tb=get_integer_from_form('team2_set1_tb')
                match.team1_set2=get_integer_from_form('team1_set2')
                match.team1_set2_tb=get_integer_from_form('team1_set2_tb')
                match.team2_set2=get_integer_from_form('team2_set2')
                match.team2_set2_tb=get_integer_from_form('team2_set2_tb')
                match.team1_set3=get_integer_from_form('team1_set3')
                match.team1_set3_tb=get_integer_from_form('team1_set3_tb')
                match.team2_set3=get_integer_from_form('team2_set3')
                match.team2_set3_tb=get_integer_from_form('team2_set3_tb')
                match.team1_won=True if request.form['match_outcome'] == 'team1_won' else False
                match.match_name=request.form['match_name']
                match.match_level=request.form['match_level']
                match.match_link=request.form['match_link']
                match.match_event=request.form['match_event']
                match.match_draw=request.form['match_draw']
                match.match_round=request.form['match_round']
                match.match_city=request.form['match_city']
                match.match_state=request.form['match_state']
                match.is_indoor=True if request.form['court_type'] == 'indoor' else False
                match.comments=request.form['match_comments']

            tennis.details = generate_match_summary(match)

    
        db.session.commit()

        redirect_url = f'/tennis?u={uid}'
        category_filter = request.args.get('category', '')
        if category_filter:
            redirect_url += f'&category={category_filter}'

        return redirect(redirect_url)
    else:
        player1_name = None
        player2_name = None
        player3_name = None
        player4_name = None
        player1 = aliased(Player)
        player2 = aliased(Player)
        player3 = aliased(Player)
        player4 = aliased(Player)

        if tennis.category == 'Match':
            match_query = db.session.query(
                Match,
                player1.first_name.label('player1_first_name'), player1.last_name.label('player1_last_name'),
                player2.first_name.label('player2_first_name'), player2.last_name.label('player2_last_name'),
                player3.first_name.label('player3_first_name'), player3.last_name.label('player3_last_name'),
                player4.first_name.label('player4_first_name'), player4.last_name.label('player4_last_name')
            ).join(player1, Match.player1 == player1.id, isouter=True) \
            .join(player2, Match.player2 == player2.id, isouter=True) \
            .join(player3, Match.player3 == player3.id, isouter=True) \
            .join(player4, Match.player4 == player4.id, isouter=True) \
            .filter(Match.tennis_id == tennis.id).first()
            if match_query:
                match, player1_first_name, player1_last_name, player2_first_name, player2_last_name, \
                player3_first_name, player3_last_name, player4_first_name, player4_last_name = match_query
                player1_name = generate_name(player1_first_name, player1_last_name)
                player2_name = generate_name(player2_first_name, player2_last_name)
                player3_name = generate_name(player3_first_name, player3_last_name)
                player4_name = generate_name(player4_first_name, player4_last_name)
        
        return render_template('tennis_update.html', tennis=tennis, match=match, player1_name=player1_name, player2_name=player2_name, player3_name=player3_name, player4_name=player4_name)

def generate_match_summary(match):
    # Extract player names
    player1_name = '' # get_brief_player_name(request.form['player1'])
    player2_name = get_brief_player_name(request.form['player2'])
    if match.type == 'D':
        player3_name = get_brief_player_name(request.form['player3'])
        player4_name = get_brief_player_name(request.form['player4'])
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

    level = generate_title(match.match_level, False)
    title = generate_title(match.match_name, True)
    round = get_match_round_abbreviation(match.match_round)
    event = extract_number_from_string(match.match_event)
    if match.match_draw == 'Consolation':
        round = f"C-{round}"

    match_summary += f" {title} {level} {event} {round}"

    return match_summary

def extract_number_from_string(input_string):
    match = re.search(r'\d+', input_string)
    if match:
        return f"U{match.group()}"
    return None

def get_brief_player_name(player):
    # Split the full name into parts
    parts = player.split()

    # Construct the formatted name
    if len(parts) >= 2:
        formatted_name = f"{parts[0]}{parts[1][0].upper()}"
    else:
        formatted_name = player.full_name  # In case only one part (unlikely for full name)

    return formatted_name

def generate_title(location_name, ignore_digits=True):
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

def get_match_round_abbreviation(round_name):
    special_rounds = {
        "Quarterfinals": "QF",
        "Semifinals": "SF",
        "Finals": "F"
    }
    
    if round_name in special_rounds:
        return special_rounds[round_name]
    else:
        return round_name[:4].upper()
    
@tennis_bp.route('/tennis/diagram')
def tennis_diagram():
    player_id = request.args.get('u')
    tennis_all = Tennis.query.filter_by(player=player_id).order_by(Tennis.date.asc()).all()

    weekly_stats = []
    
    # Initialize statistics variables
    total_records_per_week = 0
    total_duration_per_week = 0

    current_week_start, current_week_end = None, None

    # Iterate through serves and calculate statistics
    for tennis in tennis_all:
        tennis_date = tennis.date
        tennis_duration = tennis.duration
        tennis_duration = math.ceil((tennis_duration if tennis_duration is not None else 0) / 60)
        tennis_category = tennis.category

        # current_week_start, current_week_end = get_week_range(serve_date)

        # If the serve date is within the current week, update statistics
        if current_week_start is None or tennis_date < current_week_start or tennis_date > current_week_end:
            if current_week_start is not None:
                # Append statistics for the current week
                weekly_stats.append({
                    'start_date': current_week_start,
                    'end_date': current_week_end,
                    'total_records': total_records_per_week,
                    'total_duration': total_duration_per_week,
                    'total_coach': total_coach_duration_per_week,
                    'total_fitness': total_fitness_duration_per_week,
                    'total_class': total_class_duration_per_week,
                    'total_practice': total_practice_duration_per_week,
                    'total_match': total_match_duration_per_week,
                    'total_play': total_play_duration_per_week
                })

            # Set the new week range
            current_week_start, current_week_end = get_week_range(tennis_date)

            # Reset statistics for the new week
            total_records_per_week = 0
            total_duration_per_week = 0
            total_coach_duration_per_week = 0
            total_fitness_duration_per_week = 0
            total_class_duration_per_week = 0
            total_practice_duration_per_week = 0
            total_match_duration_per_week = 0
            total_play_duration_per_week = 0


        # Update statistics if the serve falls into the current week
        total_records_per_week += 1
        total_duration_per_week += tennis_duration

        if tennis_category == 'Coach':
            total_coach_duration_per_week += tennis_duration
        elif tennis_category == 'Fitness':
            total_fitness_duration_per_week += tennis_duration
        elif tennis_category == 'Group' or tennis_category == 'Private' or tennis_category == 'Semi':
            total_class_duration_per_week += tennis_duration
        elif tennis_category == 'Practice':
            total_practice_duration_per_week += tennis_duration
        elif tennis_category == 'Match':
            total_match_duration_per_week += tennis_duration
        elif tennis_category == 'Play':
            total_play_duration_per_week += tennis_duration

    # Append statistics for the last week
    if current_week_start is not None:
        weekly_stats.append({
            'start_date': current_week_start,
            'end_date': current_week_end,
            'total_records': total_records_per_week,
            'total_duration': total_duration_per_week,
            'total_coach': total_coach_duration_per_week,
            'total_fitness': total_fitness_duration_per_week,
            'total_class': total_class_duration_per_week,
            'total_practice': total_practice_duration_per_week,
            'total_match': total_match_duration_per_week,
            'total_play': total_play_duration_per_week
        })

    return render_template('tennis_diagram.html', tennis_all=tennis_all, weekly_stats=weekly_stats)