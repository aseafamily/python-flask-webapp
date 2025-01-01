from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
import json
import os
from azure.storage.fileshare import ShareFileClient
from flask_login import login_required
from datetime import datetime
from collections import Counter

news_bp = Blueprint('news', __name__)

@news_bp.route('/news')
def index():
    return render_template('news_index.html')