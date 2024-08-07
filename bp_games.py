from flask import Blueprint
from flask import render_template, request, redirect

games_bp = Blueprint('games', __name__)

@games_bp.route('/games/test')
def games_index():
    return render_template('games_test.html')