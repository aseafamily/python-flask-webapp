from flask import Blueprint
from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort
from db import db
from db_serve import Serve, ServeAnalysis, ServeStatus
from db_tennis import Tennis, TennisAnalysis, TennisStatus
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy import cast, String
from utils import test_connection, user_dict, get_week_range
from flask_login import login_required
import math

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

    if request.method == 'GET':
        tennis_all = Tennis.query.filter_by(player=player_id ).order_by(Tennis.date.desc(), Tennis.id.desc()).all()
        current_date = datetime.now() - timedelta(hours=8)

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
        return redirect('/tennis?u=' + player_id)
    
@tennis_bp.route('/tennis/delete/<int:id>')
@login_required
def tennis_delete(id):
    tennis_to_delete = Tennis.query.get_or_404(id)
    uid = request.args.get('u')

    try:
        db.session.delete(tennis_to_delete)
        db.session.commit()
        return redirect('/tennis?u=' + uid)
    except:
        return 'There was a problem deleting that task'
    
@tennis_bp.route('/tennis/update/<int:id>', methods=['GET', 'POST'])
@login_required
def tennis_update(id):
    tennis = Tennis.query.get_or_404(id)
    uid = request.args.get('u')

    if request.method == 'POST':
        tennis.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        tennis.duration = request.form['duration']
        tennis.location = request.form['location']
        tennis.category = request.form['category']
        tennis.details = request.form['details']        

        try:
            db.session.commit()
            return redirect('/tennis?u=' + uid)
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('tennis_update.html', tennis=tennis)
    
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