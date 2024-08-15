from flask import Blueprint, render_template

games_bp = Blueprint('games', __name__)

@games_bp.route('/games/tictactoe')
def tictactoe():
    return render_template('games_tictactoe.html')

@games_bp.route('/games/pong')
def pong():
    return render_template('games_pong.html')

@games_bp.route('/games/whack-a-mole')
def whack_a_mole():
    return render_template('games_whack_a_mole.html')

@games_bp.route('/games/minecraft')
def minecraft():
    return render_template('games_minecraft.html')


@games_bp.route('/games/test')
def games_index():
    return render_template('games_test.html')

@games_bp.route('/games/guess-number')
def guess_number():
    return render_template('games_guess_number.html')
