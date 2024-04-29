from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, extract

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
class Serve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    player = db.Column(db.Integer, nullable=False)
    first_serve_in = db.Column(db.Integer, default=0)
    first_serve_out = db.Column(db.Integer, default=0)
    second_serve_in = db.Column(db.Integer, default=0)
    second_serve_out = db.Column(db.Integer, default=0)
    total_first_serve = db.Column(db.Integer, default=0)
    total_second_serve = db.Column(db.Integer, default=0)
    first_serve_in_percent = db.Column(db.Integer, default=0)
    second_serve_in_percent = db.Column(db.Integer, default=0)
    total_serve = db.Column(db.Integer, default=0)
    total_serve_in = db.Column(db.Integer, default=0)
    total_serve_out = db.Column(db.Integer, default=0)
    total_serve_percent = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
    location = db.Column(db.String(200))
    comment = db.Column(db.String(1000))
    first_serve_in_deuce = db.Column(db.Integer, default=0)
    first_serve_out_deuce = db.Column(db.Integer, default=0)
    second_serve_in_deuce = db.Column(db.Integer, default=0)
    second_serve_out_deuce = db.Column(db.Integer, default=0)
    first_serve_in_percent_deuce = db.Column(db.Integer, default=0)
    second_serve_in_percent_deuce = db.Column(db.Integer, default=0)
    first_serve_in_ad = db.Column(db.Integer, default=0)
    first_serve_out_ad = db.Column(db.Integer, default=0)
    second_serve_in_ad = db.Column(db.Integer, default=0)
    second_serve_out_ad = db.Column(db.Integer, default=0)
    first_serve_in_percent_ad = db.Column(db.Integer, default=0)
    second_serve_in_percent_ad = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Serve %r>' % self.id
    
class ServeAnalysis:
    pass  # Empty class definition

class ServeStatus:
    pass  # Empty class definition

# Hardcoded dictionary mapping user IDs to names
user_dict = {
    '1': 'Andrew',
    '2': 'Emily',
    '0': 'Alex'
}

# Define a context processor to include the "u" query string parameter and the corresponding user name
@app.context_processor
def inject_user():
    user_id = request.args.get('u', '')  # Get the "u" query string parameter from the request
    user_name = user_dict.get(user_id, '')  # Get the corresponding user name from the dictionary
    return dict(u=user_id, user_name=user_name)  # Return a dictionary with the user parameter and user name


@app.route('/')
def index():
   return render_template('index.html')

# The Serve app entries

@app.route('/serve', methods=['POST', 'GET'])
def serve_index():
    player_id = request.args.get('u')

    if request.method == 'GET':
        serves_all = Serve.query.filter_by(player=player_id ).order_by(Serve.date.desc()).all()
        current_date = datetime.now() - timedelta(hours=8)

        # Query to get total serves, total duration, and count of records for the player per week
        weekly_results = Serve.query.with_entities(extract('year', Serve.date).label('year'),
                                                extract('week', Serve.date).label('week'),
                                                func.sum(Serve.total_serve),
                                                func.sum(Serve.duration),
                                                func.count(Serve.id)) \
                                    .filter(Serve.player == player_id) \
                                    .group_by('year', 'week') \
                                    .all()

        # Initialize variables for weekly data
        total_serves_weekly = 0
        total_duration_weekly = 0
        total_records_weekly = 0

        # Iterate over the weekly results and calculate totals
        for _, _, serves, duration, records in weekly_results:
            total_serves_weekly += serves or 0
            total_duration_weekly += duration or 0
            total_records_weekly += records or 0

        # Calculate the number of weeks
        num_weeks = len(weekly_results)

        # Calculate averages for weekly data
        average_serves_per_week = total_serves_weekly / num_weeks if num_weeks > 0 else 0
        average_duration_per_week = total_duration_weekly / num_weeks if num_weeks > 0 else 0
        average_records_per_week = total_records_weekly / num_weeks if num_weeks > 0 else 0

        # Query to get total serves, total duration, and count of all records for the player
        total_results = Serve.query.with_entities(func.sum(Serve.total_serve),
                                                func.sum(Serve.duration),
                                                func.count(Serve.id)) \
                                    .filter(Serve.player == player_id) \
                                    .first()

        # Extract values from the total results
        total_serves = total_results[0] or 0
        total_duration = total_results[1] or 0
        total_records = total_results[2] or 0

        # Calculate the time since the first entry
        first_entry = Serve.query.filter_by(player=player_id).order_by(Serve.date.asc()).first()
        time_since_first_entry = datetime.now() - first_entry.date if first_entry else timedelta(0)

        # Round up to days
        time_since_first_entry_rounded = timedelta(days=time_since_first_entry.days)

        # Create an instance of ServeAnalysis class
        serve_analysis = ServeAnalysis()
        serve_analysis.total_serves = total_serves
        serve_analysis.total_duration = total_duration
        serve_analysis.total_records = total_records
        serve_analysis.average_serves_per_week = average_serves_per_week
        serve_analysis.average_duration_per_week = average_duration_per_week
        serve_analysis.average_records_per_week = average_records_per_week
        serve_analysis.time_since_first_entry = time_since_first_entry_rounded

        return render_template('serve.html', serves=serves_all, now=current_date, serve_analysis=serve_analysis)
    else:
        # Retrieve form data
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        first_serve_in = request.form['first_serve_in']
        first_serve_out = request.form['first_serve_out']
        first_serve_in_percent = request.form['first_serve_in_percent']
        second_serve_in = request.form['second_serve_in']
        second_serve_out = request.form['second_serve_out']
        second_serve_in_percent = request.form['second_serve_in_percent']
        total_serve_in = request.form['total_serve_in']
        total_serve_out = request.form['total_serve_out']
        total_serve_percent = request.form['total_serve_percent']
        total_serve = request.form['total_serve']
        duration = request.form['duration']
        location = request.form['location']
        comment = request.form['comment']
        player = player_id
        first_serve_in_deuce = request.form['first_serve_in_deuce']
        first_serve_out_deuce = request.form['first_serve_out_deuce']
        first_serve_in_percent_deuce = request.form['first_serve_in_percent_deuce']
        second_serve_in_deuce = request.form['second_serve_in_deuce']
        second_serve_out_deuce = request.form['second_serve_out_deuce']
        second_serve_in_percent_deuce = request.form['second_serve_in_percent_deuce']
        first_serve_in_ad = request.form['first_serve_in_ad']
        first_serve_out_ad = request.form['first_serve_out_ad']
        first_serve_in_percent_ad = request.form['first_serve_in_percent_ad']
        second_serve_in_ad = request.form['second_serve_in_ad']
        second_serve_out_ad = request.form['second_serve_out_ad']
        second_serve_in_percent_ad = request.form['second_serve_in_percent_ad']

        # Create an instance of Serve class
        serve_instance = Serve(
            date=date,
            first_serve_in=first_serve_in,
            first_serve_out=first_serve_out,
            second_serve_in=second_serve_in,
            second_serve_out=second_serve_out,
            total_first_serve=first_serve_in + first_serve_out,
            total_second_serve=second_serve_in + second_serve_out,
            first_serve_in_percent=first_serve_in_percent,
            second_serve_in_percent=second_serve_in_percent,
            total_serve=total_serve,
            total_serve_in=total_serve_in,
            total_serve_out=total_serve_out,
            total_serve_percent=total_serve_percent,
            duration=duration,
            location=location,
            comment=comment,
            player = player,
            first_serve_in_deuce=first_serve_in_deuce,
            first_serve_out_deuce=first_serve_out_deuce,
            second_serve_in_deuce=second_serve_in_deuce,
            second_serve_out_deuce=second_serve_out_deuce,
            first_serve_in_percent_deuce=first_serve_in_percent_deuce,
            second_serve_in_percent_deuce=second_serve_in_percent_deuce,
            first_serve_in_ad=first_serve_in_ad,
            first_serve_out_ad=first_serve_out_ad,
            second_serve_in_ad=second_serve_in_ad,
            second_serve_out_ad=second_serve_out_ad,
            first_serve_in_percent_ad=first_serve_in_percent_ad,
            second_serve_in_percent_ad=second_serve_in_percent_ad
        )

        # Add the instance to the database
        db.session.add(serve_instance)
        db.session.commit()
        return redirect('/serve?u=' + player_id)
    
@app.route('/serve/delete/<int:id>')
def serve_delete(id):
    serve_to_delete = Serve.query.get_or_404(id)
    uid = request.args.get('u')

    try:
        db.session.delete(serve_to_delete)
        db.session.commit()
        return redirect('/serve?u=' + uid)
    except:
        return 'There was a problem deleting that task'

@app.route('/serve/update/<int:id>', methods=['GET', 'POST'])
def serve_update(id):
    serve = Serve.query.get_or_404(id)
    uid = request.args.get('u')

    if request.method == 'POST':
        serve.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        serve.first_serve_in = request.form['first_serve_in']
        serve.first_serve_out = request.form['first_serve_out']
        serve.first_serve_in_percent = request.form['first_serve_in_percent']
        serve.second_serve_in = request.form['second_serve_in']
        serve.second_serve_out = request.form['second_serve_out']
        serve.second_serve_in_percent = request.form['second_serve_in_percent']
        serve.total_serve_in = request.form['total_serve_in']
        serve.total_serve_out = request.form['total_serve_out']
        serve.total_serve_percent = request.form['total_serve_percent']
        serve.total_serve = request.form['total_serve']
        serve.duration = request.form['duration']
        serve.location = request.form['location']
        serve.comment = request.form['comment']
        serve.first_serve_in_deuce = request.form['first_serve_in_deuce']
        serve.first_serve_out_deuce = request.form['first_serve_out_deuce']
        serve.first_serve_in_percent_deuce = request.form['first_serve_in_percent_deuce']
        serve.second_serve_in_deuce = request.form['second_serve_in_deuce']
        serve.second_serve_out_deuce = request.form['second_serve_out_deuce']
        serve.second_serve_in_percent_deuce = request.form['second_serve_in_percent_deuce']
        serve.first_serve_in_ad = request.form['first_serve_in_ad']
        serve.first_serve_out_ad = request.form['first_serve_out_ad']
        serve.first_serve_in_percent_ad = request.form['first_serve_in_percent_ad']
        serve.second_serve_in_ad = request.form['second_serve_in_ad']
        serve.second_serve_out_ad = request.form['second_serve_out_ad']
        serve.second_serve_in_percent_ad = request.form['second_serve_in_percent_ad']

        try:
            db.session.commit()
            return redirect('/serve?u=' + uid)
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('serve_update.html', serve=serve)

@app.route('/serve/analysis')
def serve_analysis():
    player_id = request.args.get('u')
    
    # Calculate the start date of the current week (Monday)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(days=0 if today.weekday() == 6 else 1)

    # Query to get total serves, total duration, and count of records for the player per week
    results = Serve.query.with_entities(extract('year', Serve.date).label('year'),
                                        extract('week', Serve.date).label('week'),
                                        func.sum(Serve.total_serve),
                                        func.sum(Serve.duration),
                                        func.count(Serve.id)) \
                        .filter(Serve.player == player_id) \
                        .group_by('year', 'week') \
                        .all()

    # Initialize variables
    total_serves = 0
    total_duration = 0
    total_records = 0

    # Iterate over the results and calculate totals
    for _, _, serves, duration, records in results:
        total_serves += serves or 0
        total_duration += duration or 0
        total_records += records or 0

    # Calculate the number of weeks
    num_weeks = len(results)

    # Calculate averages
    average_serves_per_week = total_serves / num_weeks if num_weeks > 0 else 0
    average_duration_per_week = total_duration / num_weeks if num_weeks > 0 else 0
    average_records_per_week = total_records / num_weeks if num_weeks > 0 else 0

    # Create an instance of ServeAnalysis class
    serve_analysis = ServeAnalysis()
    serve_analysis.total_serves = total_serves
    serve_analysis.total_duration = total_duration
    serve_analysis.average_serves_per_week = average_serves_per_week
    serve_analysis.average_duration_per_week = average_duration_per_week
    serve_analysis.average_records_per_week = average_records_per_week

    # Pass the instance to the template
    return render_template('serve_analysis.html', serve_analysis=serve_analysis)

# Function to calculate the start and end of the week given a date
def get_week_range(date):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

#@app.route('/all_status')
@app.route('/serve/status')
def all_status():
    status1 = get_serve_status(1)
    status2 = get_serve_status(2)
    log0 = get_tennis_status(0)
    log1 = get_tennis_status(1)
    log2 = get_tennis_status(2)
    return render_template('all_status.html', status1=status1, status2=status2, log0=log0, log1=log1, log2=log2)

#@app.route('/serve/status')
#def serve_status():
#    status1 = get_serve_status(1)
#    status2 = get_serve_status(2)
#    return render_template('serve_status.html', status1=status1, status2=status2)

def get_serve_status(player_id):
    status = ServeStatus()
    status.player_name = user_dict.get(str(player_id), '')
    status.total_serves = calculate_total_serves(player_id)
    status.total_serve_percentage = calculate_total_serve_percentage(player_id)
    status.days_since_last_serve = calculate_days_since_last_serve(player_id)
    status.records_this_week = calculate_records_this_week(player_id)
    status.serve_this_week = calculate_serve_this_week(player_id)
    status.serve_percentage_this_week = calculate_serve_percentage_this_week(player_id)
    return status

def get_tennis_status(player_id):
    status = TennisStatus()
    status.player_name = user_dict.get(str(player_id), '')
    status.total_duration = round(calculate_total_tennis_duration(player_id)/60)
    status.weekly_duration = round(calculate_weekly_tennis_duration(player_id)/60)
    status.days_since_last_entry = calculate_days_since_last_entry(player_id)
    status.records_this_week = calculate_tennis_records_this_week(player_id)
    status.duration_this_week = round(calculate_tennis_this_week(player_id)/60)
    status.fitness_this_week = round(calculate_fitness_this_week(player_id)/60)
    return status

def calculate_total_serves(player_id):
    total_serves = Serve.query.filter_by(player=player_id).with_entities(db.func.sum(Serve.total_serve)).scalar()
    return total_serves if total_serves is not None else 0

def calculate_total_tennis_duration(player_id):
    total_serves = Tennis.query.filter_by(player=player_id).with_entities(db.func.sum(Tennis.duration)).scalar()
    return total_serves if total_serves is not None else 0

def calculate_weekly_tennis_duration(player_id):
    weekly_results = Tennis.query.with_entities(extract('year', Tennis.date).label('year'),
                                                extract('week', Tennis.date).label('week'),
                                                func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .group_by('year', 'week') \
                                    .all()
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
    
    return average_duration_per_week

def calculate_total_serve_percentage(player_id):
    total_serves = calculate_total_serves(player_id)
    total_serve_in = Serve.query.filter_by(player=player_id).with_entities(db.func.sum(Serve.total_serve_in)).scalar()
    total_serve_percentage = (total_serve_in / total_serves) * 100
    return int(total_serve_percentage)

def calculate_days_since_last_serve(player_id):
    last_serve_date = Serve.query.filter_by(player=player_id).order_by(Serve.date.desc()).first().date
    days_since_last_serve = (datetime.utcnow() - timedelta(hours=8) - last_serve_date).days
    return days_since_last_serve

def calculate_days_since_last_entry(player_id):
    last_serve_date = Tennis.query.filter_by(player=player_id).order_by(Tennis.date.desc()).first().date
    days_since_last_serve = (datetime.utcnow() - timedelta(hours=8) - last_serve_date).days
    return days_since_last_serve

def calculate_records_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    records_this_week = Serve.query.filter_by(player=player_id).filter(Serve.date.between(start_of_week, end_of_week)).count()
    return records_this_week

def calculate_tennis_records_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    records_this_week = Tennis.query.filter_by(player=player_id).filter(Tennis.date.between(start_of_week, end_of_week)).count()
    return records_this_week

def calculate_serve_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    
    serves_this_week = Serve.query.filter_by(player=player_id).filter(Serve.date.between(start_of_week, end_of_week)).all()
    
    if not serves_this_week:
        return 0  # Return 0 if no serves recorded this week
    
    total_serves_this_week = sum(serve.total_serve for serve in serves_this_week)
    return total_serves_this_week

def calculate_tennis_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    
    serves_this_week = Tennis.query.filter_by(player=player_id).filter(Tennis.date.between(start_of_week, end_of_week)).all()
    
    if not serves_this_week:
        return 0  # Return 0 if no serves recorded this week
    
    total_serves_this_week = sum(serve.duration for serve in serves_this_week)
    return total_serves_this_week

def calculate_fitness_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    
    serves_this_week = Tennis.query.filter_by(player=player_id).filter(Tennis.date.between(start_of_week, end_of_week)).filter(Tennis.category == 'Fitness').all()
    
    if not serves_this_week:
        return 0  # Return 0 if no serves recorded this week
    
    total_serves_this_week = sum(serve.duration for serve in serves_this_week)
    return total_serves_this_week

def calculate_serve_percentage_this_week(player_id):
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    serves_this_week = Serve.query.filter_by(player=player_id).filter(Serve.date.between(start_of_week, end_of_week)).all()
    
    if not serves_this_week:
        return 0  # Return 0 if no serves recorded this week
    
    total_serves_this_week = sum(serve.total_serve for serve in serves_this_week)
    total_serve_in_this_week = sum(serve.total_serve_in for serve in serves_this_week)
    
    if total_serves_this_week == 0:
        return 0  # Avoid division by zero
    
    serve_percentage_this_week = (total_serve_in_this_week / total_serves_this_week) * 100
    return int(serve_percentage_this_week)  # Cast to integer

@app.route('/serve/diagram')
def serve_diagram():
    player_id = request.args.get('u')
    serves_all = Serve.query.filter_by(player=player_id).order_by(Serve.date.asc()).all()

    weekly_stats = []
    
    # Initialize statistics variables
    total_serves_per_week = 0
    total_records_per_week = 0
    total_duration_per_week = 0

    current_week_start, current_week_end = None, None

    # Iterate through serves and calculate statistics
    for serve in serves_all:
        serve_date = serve.date
        serve_duration = serve.duration
        total_server = serve.total_serve

        # current_week_start, current_week_end = get_week_range(serve_date)

        # If the serve date is within the current week, update statistics
        if current_week_start is None or serve_date < current_week_start or serve_date > current_week_end:
            if current_week_start is not None:
                # Append statistics for the current week
                weekly_stats.append({
                    'start_date': current_week_start,
                    'end_date': current_week_end,
                    'total_serves': total_serves_per_week,
                    'total_records': total_records_per_week,
                    'total_duration': total_duration_per_week
                })

            # Set the new week range
            current_week_start, current_week_end = get_week_range(serve_date)

            # Reset statistics for the new week
            total_serves_per_week = 0
            total_records_per_week = 0
            total_duration_per_week = 0

        # Update statistics if the serve falls into the current week
        total_serves_per_week += total_server
        total_records_per_week += 1
        total_duration_per_week += serve_duration

    # Append statistics for the last week
    if current_week_start is not None:
        weekly_stats.append({
            'start_date': current_week_start,
            'end_date': current_week_end,
            'total_serves': total_serves_per_week,
            'total_records': total_records_per_week,
            'total_duration': total_duration_per_week
        })

    return render_template('serve_diagram.html', serves=serves_all, weekly_stats=weekly_stats)

# The tennis stuff =========================================================================

class Tennis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    player = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float)
    location = db.Column(db.String(200))
    category = db.Column(db.String(200))
    details = db.Column(db.String(200))

    def __repr__(self):
        return '<Tennis %r>' % self.id

class TennisAnalysis:
    pass  # Empty class definition

class TennisStatus:
    pass  # Empty class definition

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Tennis.query.with_entities(Tennis.category).distinct().order_by(Tennis.category).all()
    categories_list = [category[0] for category in categories]
    return jsonify(categories_list)

@app.route('/tennis', methods=['POST', 'GET'])
def tennis_index():
    player_id = request.args.get('u')

    if request.method == 'GET':
        tennis_all = Tennis.query.filter_by(player=player_id ).order_by(Tennis.date.desc()).all()
        current_date = datetime.now() - timedelta(hours=8)

        weekly_results = Tennis.query.with_entities(extract('year', Tennis.date).label('year'),
                                                extract('week', Tennis.date).label('week'),
                                                func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .group_by('year', 'week') \
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
                                    .filter(Tennis.category == 'Fitness') \
                                    .first()
        
        total_fitness_duration = total_fitness_result[0] or 0

        # Calculate fitness weekly
        fitness_weekly_results = Tennis.query.with_entities(extract('year', Tennis.date).label('year'),
                                                extract('week', Tennis.date).label('week'),
                                                func.sum(Tennis.duration),
                                                func.count(Tennis.id)) \
                                    .filter(Tennis.player == player_id) \
                                    .filter(Tennis.category == 'Fitness') \
                                    .group_by('year', 'week') \
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
    
@app.route('/tennis/delete/<int:id>')
def tennis_delete(id):
    tennis_to_delete = Tennis.query.get_or_404(id)
    uid = request.args.get('u')

    try:
        db.session.delete(tennis_to_delete)
        db.session.commit()
        return redirect('/tennis?u=' + uid)
    except:
        return 'There was a problem deleting that task'
    
@app.route('/tennis/update/<int:id>', methods=['GET', 'POST'])
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

# The TODO App entries =====================================================================

@app.route('/todo', methods=['POST', 'GET'])
def todo_index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks)


@app.route('/todo/delete/<int:id>')
def todo_delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'

@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def todo_update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('todo_update.html', task=task)
    
@app.route('/serve/db')
def serve_db():
    try:
        return send_file('test.db', as_attachment=True)
    except Exception as e:
        return str(e)

# The Serve practice App entries

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)