from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy import cast, String
from db import db, db_uri
from todo import todo_bp
from serve import serve_bp
from tennis import tennis_bp
from games import games_bp
from match import match_bp
from utils import user_dict, generate_title
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm
from user import User, users
from tools import tools_bp

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,  # Adjust as needed
    'pool_recycle': 3600,  # Optional: Recycle connections after 1 hour
    'pool_timeout': 30,  # Optional: Maximum time to wait for a connection from the pool
}

db.init_app(app)

app.register_blueprint(tennis_bp)
app.register_blueprint(serve_bp)
app.register_blueprint(todo_bp)
app.register_blueprint(games_bp)
app.register_blueprint(match_bp)
app.register_blueprint(tools_bp)

# for login
app.config['SECRET_KEY'] = '48e7a59dca9d6c13b0e7e51b7ee6e2a5759c8e1dbb3a0f83'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.template_filter('generate_acronym')
def generate_acronym(location_name):
    # Check if location_name is already an acronym (less than four uppercase characters)
    if len(location_name) <= 4 and location_name.isupper():
        return location_name

    # Words to skip
    skip_words = {'a', 'an', 'the', 'and'}

    # Split the location name into words
    words = location_name.split()

    # Initialize acronym
    acronym = ""

    # Build acronym from first letters of each word (up to 4 characters)
    for word in words:
        if word.lower() not in skip_words:
            acronym += word[0].upper()

            # Break loop if acronym length reaches 4 characters
            if len(acronym) >= 4:
                break

    return acronym

@app.template_filter('divide_and_format')
def divide_and_format(value):
    try:
        # Divide the value by 100
        result = value / 100
        
        # Format the result to two decimal places
        formatted_result = f"{result:.2f}"
        
        return formatted_result
    
    except TypeError:
        # Handle the case where the input is not an integer
        return None

@app.template_filter('filter_none')
def filter_none(variables):
    return [var for var in variables if var is not None]

@app.template_filter('short_name')
def short_name(variables):
    return generate_title(variables)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next')  # Get the 'next' query parameter
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Define a context processor to include the "u" query string parameter and the corresponding user name
@app.context_processor
def inject_user():
    user_id = request.args.get('u', '')  # Get the "u" query string parameter from the request
    user_name = user_dict.get(user_id, '')  # Get the corresponding user name from the dictionary
    return dict(u=user_id, user_name=user_name)  # Return a dictionary with the user parameter and user name

@app.route('/')
def index():
   return render_template('index.html', current_user=current_user)

# Route to handle requests for favicon.ico
@app.route('/favicon.ico')
def favicon():
    abort(404)

@app.route("/test/mansonry")
def test_mansonry():
    return render_template("test-masonry-js.html")

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)