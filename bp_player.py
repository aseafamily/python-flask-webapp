from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from sqlalchemy import or_
from db_player import Player
from db_match import Match
from db import db
from datetime import datetime

player_bp = Blueprint('player', __name__)

@player_bp.route('/player/s')
def player_search():
    term = request.args.get('term', '')
    user_id = request.args.get('u', '')

    # Create a base query to search for players
    query = db.session.query(Player).distinct()

    # Always apply name filter
    search_words = term.split()
    for word in search_words:
        query = query.filter(
            or_(
                Player.first_name.ilike(f'%{word}%'),
                Player.last_name.ilike(f'%{word}%')
            )
        )

    # Apply user_id filter only if term is less than 7 characters
    if len(term) < 7:
        query = query.join(Match, or_(
            Match.player1 == Player.id,
            Match.player2 == Player.id,
            Match.player3 == Player.id,
            Match.player4 == Player.id
        )).filter(Match.player1 == user_id)

    # Limit the results to 10 players
    players = query.limit(10).all()

    # Format the results
    results = [
        {
            'id': player.id,
            'name': f"{player.first_name} {player.last_name}".strip()
        }
        for player in players
    ]

    return jsonify(results)

@player_bp.route('/player', methods=['GET'])
def player_list():
    search_query = request.args.get('search', '').strip()
    
    # Fetch players from the database and sort by first name and last name
    query = db.session.query(Player).order_by(Player.first_name, Player.last_name)
    
    if search_query:
        # Filter players based on the search query
        query = query.filter(
            Player.first_name.ilike(f'%{search_query}%') | 
            Player.last_name.ilike(f'%{search_query}%')
        )
    
    players = query.all()

    # Group players by the first letter of their first name
    grouped_players = {}
    for player in players:
        first_letter = player.first_name[0].upper()
        if first_letter not in grouped_players:
            grouped_players[first_letter] = []
        grouped_players[first_letter].append(player)

    # Get today's date
    today = datetime.now()

    return render_template('player_list.html', grouped_players=grouped_players, search_query=search_query, today=today)

@player_bp.route('/player/<int:player_id>')
def player_detail(player_id):
    # Fetch the player by ID from the database
    player = db.session.query(Player).filter_by(id=player_id).first()

    if player is None:
        return "Player not found", 404

    # Render the player detail template with the player's data
    return render_template('player_detail.html', player=player)

@player_bp.route('/player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    player = db.session.query(Player).filter_by(id=player_id).first()

    if player is None:
        return "Player not found", 404

    # Update player fields from the request
    player.first_name = request.form.get('first_name', player.first_name)
    player.last_name = request.form.get('last_name', player.last_name)
    player.gender = request.form.get('gender', player.gender)
    player.birthday = request.form.get('birthday', player.birthday)
    player.year_graduation = request.form.get('year_graduation', player.year_graduation)
    player.utr_profile = request.form.get('utr_profile', player.utr_profile)
    player.usta_profile = request.form.get('usta_profile', player.usta_profile)
    player.usta_id = request.form.get('usta_id', player.usta_id)
    player.utr = request.form.get('utr', player.utr)
    player.wtn = request.form.get('wtn', player.wtn)
    player.usta = request.form.get('usta', player.usta)
    player.utr_date = request.form.get('utr_date', player.utr_date)
    player.wtn_date = request.form.get('wtn_date', player.wtn_date)
    player.usta_date = request.form.get('usta_date', player.usta_date)
    player.city = request.form.get('city', player.city)
    player.state = request.form.get('state', player.state)
    player.country = request.form.get('country', player.country)
    player.note = request.form.get('note', player.note)

    db.session.commit()

    return redirect(url_for('player.player_detail', player_id=player.id))

@player_bp.route('/player/<int:player_id>/delete', methods=['POST'])
def delete_player(player_id):
    player = db.session.query(Player).filter_by(id=player_id).first()

    if player is None:
        return "Player not found", 404

    db.session.delete(player)
    db.session.commit()

    return redirect(url_for('player.player_list'))