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
from utils import test_connection, user_dict, get_week_range, get_client_time
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
    return render_template('match.html')