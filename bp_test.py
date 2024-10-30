from flask import Blueprint, jsonify, request
import markdown2
import os
import json
import re
import random
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

test_bp = Blueprint('test', __name__)

# List of YouTube Data API keys
API_KEYS = [
    'AIzaSyCBQC-t1rS7_AfTupodVZmAH9ey6eooCF0',
    'AIzaSyAvwBviIPoESxTjciXlwNxeD2LQ_agjfs8',
    'AIzaSyCqJZrA4X0UJIqWXR1E_h3e48K2i3pvCuw',
    'AIzaSyBK-dnlZDveYyXoddWCxcWygFMalPsmH_0',
    'AIzaSyAU3SYYMw9ayggliC0fW7mNP2kjn6il9tc'
]
current_api_key_index = 0

def get_current_api_key():
    return API_KEYS[current_api_key_index]

def rotate_api_key():
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(API_KEYS)

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
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'channels.json')  # Construct the full path

    channels = load_channels(file_path)
    all_videos_info = []
    total_duration_seconds = 0

    if channels:
        for channel in channels:
            channel_id = channel['channel_id']
            min_minutes = channel.get('min_minutes', 0)
            max_minutes = channel.get('max_minutes', float('inf'))
            last_hours = channel.get('last_hours', 0)
            last_number = channel.get('last_number', 5)

            videos_info, total_duration = get_last_five_regular_videos(channel_id, min_minutes=min_minutes, max_minutes=max_minutes, last_hours=last_hours, last_number=last_number)
            all_videos_info.extend(videos_info)
            total_duration_seconds += total_duration  # Accumulate total duration

        # Shuffle the combined list of video information
        random.shuffle(all_videos_info)
        total_video_count = len(all_videos_info)
        total_duration_iso = format_duration(total_duration_seconds)

        return jsonify({
            "status": "success",
            "total_videos": total_video_count,
            "total_duration": total_duration_iso,
            "videos": all_videos_info
        }), 200
    else:
        return jsonify({"status": "error", "message": "No channels loaded."}), 404

def parse_iso_duration(duration):
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def format_duration(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_parts = []
    if hours > 0:
        duration_parts.append(f"{hours}H")
    if minutes > 0:
        duration_parts.append(f"{minutes}M")
    if seconds > 0:
        duration_parts.append(f"{seconds}S")
    return "PT" + "".join(duration_parts)

def get_video_details(video_ids):
    global current_api_key_index
    youtube = build('youtube', 'v3', developerKey=get_current_api_key())
    video_details_request = youtube.videos().list(
        part='contentDetails,snippet',
        id=','.join(video_ids)
    )
    try:
        return video_details_request.execute()
    except HttpError as e:
        if e.resp.status == 403:  # Quota exceeded
            rotate_api_key()  # Rotate to the next API key
            if current_api_key_index == 0:  # If we have cycled through all keys
                raise Exception("All API keys have been exhausted. Please try again later.")
            return get_video_details(video_ids)  # Retry with the new key
        else:
            raise  # Raise other errors

def get_last_five_regular_videos(channel_id, min_minutes=0, max_minutes=float('inf'), last_hours=0, last_number=5):
    global current_api_key_index
    youtube = build('youtube', 'v3', developerKey=get_current_api_key())
    time_threshold = datetime.utcnow() - timedelta(hours=last_hours)

    # Request to retrieve the latest videos from the channel
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=10,  # Request more than 5 to account for filtering out Shorts
        order='date',
        type='video'
    )
    
    try:
        response = request.execute()
    except HttpError as e:
        if e.resp.status == 403:  # Quota exceeded
            rotate_api_key()  # Rotate to the next API key
            if current_api_key_index == 0:  # If we have cycled through all keys
                raise Exception("All API keys have been exhausted. Please try again later.")
            return get_last_five_regular_videos(channel_id, min_minutes, max_minutes, last_hours, last_number)  # Retry with the new key
        else:
            raise  # Raise other errors

    video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
    
    # Get details (including duration) of each video in a single request
    if video_ids:
        video_details_response = get_video_details(video_ids)
    else:
        return []

    regular_videos = []
    total_duration_seconds = 0
    
    for item in video_details_response['items']:
        if 'duration' in item['contentDetails']:
            duration = item['contentDetails']['duration']
            total_seconds = parse_iso_duration(duration)
            total_minutes = total_seconds / 60
            
            upload_time = item['snippet']['publishedAt']
            upload_time = datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%SZ")

            if (min_minutes <= total_minutes <= max_minutes) and (upload_time >= time_threshold):
                video_info = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'duration': duration,
                    'published_at': upload_time.isoformat(),
                    'channel_title': item['snippet']['channelTitle']
                }
                regular_videos.append(video_info)
                total_duration_seconds += total_seconds  # Accumulate total duration

    return regular_videos[:last_number], total_duration_seconds

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
