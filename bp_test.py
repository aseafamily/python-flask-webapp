from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
import markdown2
import os
import json
import re
import random
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from azure.storage.fileshare import ShareFileClient
from flask_login import login_required

test_bp = Blueprint('test', __name__)

# List of YouTube Data API keys
API_KEYS = [
    'AIzaSyCBQC-t1rS7_AfTupodVZmAH9ey6eooCF0',
    'AIzaSyAvwBviIPoESxTjciXlwNxeD2LQ_agjfs8',
    'AIzaSyCqJZrA4X0UJIqWXR1E_h3e48K2i3pvCuw',
    'AIzaSyBK-dnlZDveYyXoddWCxcWygFMalPsmH_0',
    'AIzaSyAU3SYYMw9ayggliC0fW7mNP2kjn6il9tc',
    'AIzaSyByzU-kn4lFEFnDaz66sUr_Ky3Oia0gSes',
    'AIzaSyCyp6WOJol8JQ1_6M0x4njkr9Y2nierC9E',
    'AIzaSyCEdLlTKDpwfcsb2ydeYVkzBKH-KBReY7Q',
    'AIzaSyA8Dm7MpI-XcNajSQ4zJJyJMpdNWVtz5Dw',
    'AIzaSyAYipHYSpqqkKXiQ4av8C-0QTRVWW8WObo',
    'AIzaSyDOibP9BHXARLC0yuAr85TkG1VPrSFx2Q8',
    'AIzaSyAEXepoY2SQg9dx3DhIhIh-JcEznaFZOc0'
]
current_api_key_index = 0

# Flag to check if the keys have been shuffled
keys_shuffled = False

def get_current_api_key():
    global keys_shuffled
    if not keys_shuffled:
        random.shuffle(API_KEYS)  # Shuffle the API keys
        keys_shuffled = True  # Set the flag to True after shuffling
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
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #file_path = os.path.join(current_dir, 'channels.json')  # Construct the full path

    #channels = load_channels_local(file_path)
    channels = load_channels() 
    all_videos_info = []
    
    if channels:
        for channel in channels:
            channel_id = channel['channel_id']
            min_minutes = channel.get('min_minutes', 0)
            max_minutes = channel.get('max_minutes', float('inf'))
            last_hours = channel.get('last_hours', 0)
            last_number = channel.get('last_number', 5)
            is_active = channel.get('is_active', True)  # Default value is True

            if is_active:  # Check if the channel is active
                videos_info = get_last_five_regular_videos(channel_id, min_minutes=min_minutes, max_minutes=max_minutes, last_hours=last_hours, last_number=last_number)
                all_videos_info.extend(videos_info)
            else:
                print(f"Channel {channel_id} is not active, skipping.")

        # Shuffle the combined list of video information
        random.shuffle(all_videos_info)
        total_video_count = len(all_videos_info)
        
        return jsonify({
            "status": "success",
            "total_videos": total_video_count,
            "videos": all_videos_info
        }), 200
    else:
        return jsonify({"status": "error", "message": "No channels loaded."}), 404

def load_channels():
    """Load and return the configuration from Azure Blob Storage."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    file_share_name = "bhmfiles"
    directory_name = "youtube"  # Updated directory name
    filename = "channels.json"   # Updated file name

    file_path = f"{directory_name}/{filename}"

    file_client = ShareFileClient.from_connection_string(
        connection_string, file_share_name, file_path)

    # Download the blob data
    download = file_client.download_file()
    downloaded_bytes = download.readall()
    file_content = downloaded_bytes.decode('utf-8')

    # Parse and return the JSON data
    data = json.loads(file_content)
    return data.get('channels', [])

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
        part='id,snippet',  # Include snippet to get title and published date
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

    regular_videos = []
    
    for item in response['items']:
        published_at_str = item['snippet']['publishedAt']
        published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")  # Parse the published date

        if published_at >= time_threshold:
            if item['id']['kind'] == 'youtube#video':
                video_info = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],  # Get title from snippet
                    'published_at': item['snippet']['publishedAt']  # Get published date
                }
                regular_videos.append(video_info)

    return regular_videos[:last_number]  # Return the requested number of videos

def load_channels_local(file_path):
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

def save_channels(channels_data):
    """Save the channels data to a JSON file."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    file_share_name = "bhmfiles"
    directory_name = "youtube"
    filename = "channels.json"

    file_path = f"{directory_name}/{filename}"

    file_client = ShareFileClient.from_connection_string(
        connection_string, file_share_name, file_path)

    # Convert channels data to JSON format
    data_to_save = {"channels": channels_data}
    json_data = json.dumps(data_to_save, indent=4)

    # Upload the JSON data to Azure Blob Storage
    file_client.upload_file(json_data)

@test_bp.route('/channels', methods=['GET', 'POST'])
@login_required
def channels():
    if request.method == 'POST':
        # Handle adding a new channel
        new_channel = {
            'channel_title': request.form['title'],
            'channel_id': request.form['id'],  # Keep as string
            'last_hours': int(request.form['last_hours']),
            'last_number': int(request.form['last_number']),
            'is_active': request.form.get('is_active') == 'on'
        }
        channels_data = load_channels()  # Function to load channels.json
        channels_data.append(new_channel)
        save_channels(channels_data)  # Function to save channels.json
        return redirect(url_for('test.channels'))

    channels_data = load_channels()  # Load existing channels
    channels_data.sort(key=lambda c: c['channel_title'].lower())  # Sort channels by title (case insensitive)
    return render_template('channels.html', channels=channels_data)

@test_bp.route('/channels/update/<string:channel_id>', methods=['GET', 'POST'])  # Change to string
@login_required
def update_channel(channel_id):
    channels_data = load_channels()
    channel = next((c for c in channels_data if c['channel_id'] == channel_id), None)  # Keep as string

    if request.method == 'POST':
        # Update channel details
        channel['channel_title'] = request.form['title']
        channel['last_hours'] = int(request.form['last_hours'])
        channel['last_number'] = int(request.form['last_number'])
        # Check if is_active is in the form data
        channel['is_active'] = request.form.get('is_active') == 'on'  # Set to True if checked, False otherwise
        save_channels(channels_data)
        return redirect(url_for('test.channels'))

    return render_template('channel_update.html', channel=channel)

@test_bp.route('/channels/delete/<string:channel_id>', methods=['POST'])  # Change to string
@login_required
def delete_channel(channel_id):
    channels_data = load_channels()
    channels_data = [c for c in channels_data if c['channel_id'] != channel_id]  # Keep as string
    save_channels(channels_data)
    return redirect(url_for('test.channels'))