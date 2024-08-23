from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from db_player import Player
from db_match import Match
from db import db

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