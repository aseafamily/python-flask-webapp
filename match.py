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
from utils import test_connection, user_dict, get_week_range, get_client_time, get_match_round_abbreviation
from flask_login import login_required
import math
from sqlalchemy.orm import aliased
import re
import os
from azure.storage.fileshare import ShareFileClient, ShareServiceClient

match_bp = Blueprint('match', __name__)

@match_bp.route('/match')
@login_required
def match_index():
    player_id = request.args.get('u')
    player1 = aliased(Player)
    player2 = aliased(Player)
    player3 = aliased(Player)
    player4 = aliased(Player)

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
    .filter(Match.player1 == player_id) \
    .order_by(desc(Match.date), desc(Match.id)) \
    .all()

    results = []
    last_match_name = None
    for match in match_query:
        if match.Match.type == 'S':
            team1_name = f"{match.player1_first_name} {match.player1_last_name}"
            team2_name = f"{match.player2_first_name} {match.player2_last_name}"
        else:  # Assuming 'Doubles'
            team1_name = get_name_short(match.player1_first_name, match.player1_last_name) + " / " + get_name_short(match.player3_first_name, match.player3_last_name)
            team2_name = get_name_short(match.player2_first_name, match.player2_last_name) + " / " + get_name_short(match.player4_first_name, match.player4_last_name)
            
        if match.Match.player1_seed:
                team1_name += f" [{match.Match.player1_seed}]"
        if match.Match.player2_seed:
                team2_name += f" [{match.Match.player2_seed}]"

        round_name = get_match_round_abbreviation(match.Match)

        match_data = {
            'match': match.Match,
            'player1_first_name': match.player1_first_name,
            'player1_last_name': match.player1_last_name,
            'player2_first_name': match.player2_first_name,
            'player2_last_name': match.player2_last_name,
            'player3_first_name': match.player3_first_name,
            'player3_last_name': match.player3_last_name,
            'player4_first_name': match.player4_first_name,
            'player4_last_name': match.player4_last_name,
            'team1_name': team1_name,
            'team2_name': team2_name,
            'round_name': round_name,
            'show_match_name': match.Match.match_name != last_match_name
        }
        results.append(match_data)
        last_match_name = match.Match.match_name

    return render_template('match.html', results=results)

def get_name_short(first_name, last_name):
    name = f"{first_name} {last_name[0]}" if last_name else first_name
    return name if name else ''