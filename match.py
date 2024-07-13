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
from utils import test_connection, user_dict, get_week_range, get_client_time, get_match_round_abbreviation, generate_title, extract_number_from_string
from flask_login import login_required
import math
from sqlalchemy.orm import aliased
import re
import os
from azure.storage.fileshare import ShareFileClient, ShareServiceClient
from azure.core.exceptions import ResourceNotFoundError
from io import BytesIO

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

        including_year = match.Match.match_event is not None and "Adults" in match.Match.match_event
        tournament_logo = generate_title(match.Match.match_name, True, including_year)

        event_name = extract_number_from_string(match.Match.match_event)

        team1_games = (match.Match.team1_set1 if match.Match.team1_set1 else 0) + (match.Match.team1_set2 if match.Match.team1_set2 else 0) + (match.Match.team1_set3 if match.Match.team1_set3 else 0)
        team2_games = (match.Match.team2_set1 if match.Match.team2_set1 else 0) + (match.Match.team2_set2 if match.Match.team2_set2 else 0) + (match.Match.team2_set3 if match.Match.team2_set3 else 0)
        diff_games = team1_games - team2_games
        if diff_games < 0:
             diff_games = diff_games * -1
        games = team1_games if match.Match.team1_won else team2_games
        diff_indicator = (diff_games / games) if games else 0
        diff_indicator = diff_indicator * 100 * 0.95 + 5

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
            'tournament_logo': tournament_logo,
            'event_name': event_name,
            'diff_indicator': diff_indicator,
            'show_match_name': match.Match.match_name != last_match_name
        }
        results.append(match_data)
        last_match_name = match.Match.match_name

    return render_template('match.html', results=results)

def get_name_short(first_name, last_name):
    name = f"{first_name} {last_name[0]}" if last_name else first_name
    return name if name else ''

@match_bp.route('/match/logo/<string:image_id>')
def get_logo(image_id):
    file_share_name = "bhmfiles"
    folder_name = "tennis/logo"
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    try:
        
        service_client = ShareServiceClient.from_connection_string(connection_string)
        directory_client = service_client.get_share_client(file_share_name).get_directory_client(folder_name)
        file_client = directory_client.get_file_client(f"{image_id}.png")
        stream = file_client.download_file()
        # Create a BytesIO object to store the downloaded content
        content = BytesIO()
        content.write(stream.readall())

        # Seek back to the beginning of the BytesIO object
        content.seek(0)

        # Return the image file
        return send_file(content, mimetype='image/png')

    except ResourceNotFoundError:
        abort(404)

@match_bp.route('/match/<int:id>')
@login_required
def match_one(id):
     # tempalte page
     # https://www.sofascore.com/tennis/match/sun-vekic/QmvsHdDb#id:12460178

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
    .filter(Match.id == id) \
    .first()

    including_year = match_query.Match.match_event is not None and "Adults" in match_query.Match.match_event
    tournament_logo = generate_title(match_query.Match.match_name, True, including_year)

    match_data = {
        'Match': match_query.Match,
        'player1_first_name': match_query.player1_first_name,
        'player1_last_name': match_query.player1_last_name,
        'player2_first_name': match_query.player2_first_name,
        'player2_last_name': match_query.player2_last_name,
        'player3_first_name': match_query.player3_first_name,
        'player3_last_name': match_query.player3_last_name,
        'player4_first_name': match_query.player4_first_name,
        'player4_last_name': match_query.player4_last_name,
        'tournament_logo': tournament_logo
    }

    # get scores
    file_share_name = "bhmfiles"
    folder_name = f"tennis/{match_query.Match.tennis_id}"
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    scores_html = ''
    try:
        service_client = ShareServiceClient.from_connection_string(connection_string)
        directory_client = service_client.get_share_client(file_share_name).get_directory_client(folder_name)
        file_name = "scores.html"
        file_client = directory_client.get_file_client(file_name)
        # Check if the file exists by trying to get its properties
        file_client.get_file_properties()

        # If the file exists, download its content
        download = file_client.download_file()
        scores_html = download.readall().decode('utf-8')
    except Exception as e:
        print(f"An error occurred when getting {folder_name}/{file_name}: {e}")


    return render_template('match_one.html', match_data = match_data, scores_html=scores_html)