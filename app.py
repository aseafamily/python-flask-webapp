from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy import cast, String
from db import db, db_uri
from todo import todo_bp
from serve import serve_bp
from tennis import tennis_bp
from utils import user_dict

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

# Define a context processor to include the "u" query string parameter and the corresponding user name
@app.context_processor
def inject_user():
    user_id = request.args.get('u', '')  # Get the "u" query string parameter from the request
    user_name = user_dict.get(user_id, '')  # Get the corresponding user name from the dictionary
    return dict(u=user_id, user_name=user_name)  # Return a dictionary with the user parameter and user name

@app.route('/')
def index():
   return render_template('index.html')

# Route to handle requests for favicon.ico
@app.route('/favicon.ico')
def favicon():
    abort(404)

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)