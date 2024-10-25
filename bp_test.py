from flask import Blueprint, jsonify, request
import markdown2
import os
import json
import re
import random
from datetime import datetime, timedelta
from googleapiclient.discovery import build

test_bp = Blueprint('test', __name__)

@test_bp.route('/test/markdown', methods=['GET', 'POST'])
def markdown_form():
    initial_content = "# Hello World\n\nThis is a simple **Hello World** markdown example.\n\n- Item 1\n- Item 2\n- Item 3\n\nEnjoy writing markdown with SimpleMDE!"

    if request.method == 'POST':
        content = request.form['content']
        html_content = markdown2.markdown(content)
        return render_template('test_display_markdown.html', content=html_content)
    return render_template('test_markdown.html', initial_content=initial_content)

@test_bp.route('/test/tennis_match_control', methods=['GET', 'POST'])
def tennis_match_control():
    return render_template('test_tennis_match_control.html')


@test_bp.route('/api/youtube', methods=['GET'])
def youtube_api():
    file_path = 'channels.json'  # Adjust the path if needed
    channels = load_channels(file_path)
    all_video_ids = []

    if channels:
        for channel in channels:
            channel_id = channel['channel_id']
            min_minutes = channel.get('min_minutes', 0)
            max_minutes = channel.get('max_minutes', float('inf'))
            last_hours = channel.get('last_hours', 0)
            last_number = channel.get('last_number', 5)

            videos = get_last_five_regular_videos(channel_id, min_minutes=min_minutes, max_minutes=max_minutes, last_hours=last_hours, last_number=last_number)
            all_video_ids.extend(videos)

        # Shuffle the combined list of video IDs
        random.shuffle(all_video_ids)
        return jsonify({"status": "success", "video_ids": all_video_ids}), 200
    else:
        return jsonify({"status": "error", "message": "No channels loaded."}), 404

def parse_duration(duration):
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def get_last_five_regular_videos(channel_id, min_minutes=0, max_minutes=float('inf'), last_hours=0, last_number=5):
    youtube = build('youtube', 'v3', developerKey="AIzaSyAU3SYYMw9ayggliC0fW7mNP2kjn6il9tc")
    time_threshold = datetime.utcnow() - timedelta(hours=last_hours)

    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=10,
        order='date',
        type='video'
    )
    
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
    
    video_details_request = youtube.videos().list(
        part='contentDetails,snippet',
        id=','.join(video_ids)
    )
    video_details_response = video_details_request.execute()

    regular_video_ids = []
    
    for item in video_details_response['items']:
        if 'duration' in item['contentDetails']:
            duration = item['contentDetails']['duration']
            total_seconds = parse_duration(duration)
            total_minutes = total_seconds / 60
            
            upload_time = item['snippet']['publishedAt']
            upload_time = datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%SZ")

            if (min_minutes <= total_minutes <= max_minutes) and (upload_time >= time_threshold):
                regular_video_ids.append(item['id'])

    return regular_video_ids[:last_number]

def load_channels(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('channels', [])
    except FileNotFoundError:
        print("The file was not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []
