from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import json
import os
from azure.storage.fileshare import ShareFileClient, ShareDirectoryClient
from flask_login import login_required

lt_bp = Blueprint('lt', __name__)

# Load configuration file
with open('lt_config.json', 'r') as f:
    config = json.load(f)

def read_logs(log_type, user_id):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    file_share_name = "bhmfiles"
    directory_name = "logs"
    filename = f"{log_type}_{user_id}_logs.json"

    file_path = f"{directory_name}/{filename}"

    # Create a ShareFileClient to interact with the file
    file_client = ShareFileClient.from_connection_string(
        connection_string, file_share_name, file_path)

    logs = []

    try:
        # Download the file content
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        file_content = downloaded_bytes.decode('utf-8')

        # Read each line as a separate JSON object
        logs = [json.loads(line) for line in file_content.splitlines()]

    except Exception as e:
        print(f"An error occurred: {e}")

    return logs

def read_local_logs(log_type, user_id):
    filename = f"{log_type}_{user_id}_logs.json"
    logs = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            logs = [json.loads(line) for line in f]
    return logs

def write_logs(log_type, logs, user_id):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    file_share_name = "bhmfiles"
    directory_name = "logs"
    filename = f"{log_type}_{user_id}_logs.json"
    file_path = f"{directory_name}/{filename}"

    # Create a ShareFileClient to interact with the file
    file_client = ShareFileClient.from_connection_string(
        connection_string, file_share_name, file_path)

    try:
        # Convert logs to JSON lines format
        log_content = "\n".join(json.dumps(log) for log in logs) + '\n'
        log_content_bytes = log_content.encode('utf-8')
        file_size = len(log_content_bytes)
        
        # Create the file with the necessary size
        file_client.create_file(size=file_size)
        
        # Upload the log content to the file
        file_client.upload_range(data=log_content_bytes, offset=0, length=file_size)
        
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def write_local_logs(log_type, logs, user_id):
    filename = f"{log_type}_{user_id}_logs.json"
    with open(filename, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')

@lt_bp.route('/lt')
@login_required
def index():
    log_types = config['log_types']
    return render_template('lt_index.html', log_types=log_types)

@lt_bp.route('/lt/<log_type>', methods=['GET'])
@login_required
def log_form(log_type):
    if log_type in config['log_types']:
        user_id = request.args.get('u', '')
        log_config = config['log_types'][log_type]
        logs = read_logs(log_type, user_id)
        return render_template('lt_log_form.html', log_type=log_type, log_config=log_config, logs=logs)
    return "Log type not found", 404

@lt_bp.route('/lt/<log_type>', methods=['POST'])
def submit_log(log_type):
    if log_type in config['log_types']:
        user_id = request.args.get('u', '')
        log_data = request.form.to_dict()
        logs = read_logs(log_type, user_id)

        # Add a new ID to the log data
        new_id = max([log.get('id', 0) for log in logs], default=0) + 1
        log_data['id'] = new_id

        logs.append(log_data)
        write_logs(log_type, logs, user_id)
        redirect_url = url_for('lt.log_form', log_type=log_type)
        redirect_url += "?u=" + request.args.get('u', '')
        return redirect(redirect_url)
    return "Log type not found", 404

@lt_bp.route('/lt/update/<log_type>/<int:log_id>', methods=['GET'])
def update_form(log_type, log_id):
    if log_type in config['log_types']:
        log_config = config['log_types'][log_type]
        user_id = request.args.get('u', '')
        logs = read_logs(log_type, user_id)

        log = next((entry for entry in logs if int(entry.get('id', 0)) == log_id), None)
        if log:
            return render_template('lt_update_form.html', log_type=log_type, log_config=log_config, log=log, log_id=log_id)
        return "Log entry not found", 404
    return "Log type not found", 404

@lt_bp.route('/lt/update/<log_type>/<int:log_id>', methods=['POST'])
def update_log(log_type, log_id):
    if log_type in config['log_types']:
        user_id = request.args.get('u', '')

        log_data = request.form.to_dict()
        log_data["id"] = log_id

        logs = read_logs(log_type, user_id)

        logs = [log_data if int(log.get('id', 0)) == log_id else log for log in logs]
        write_logs(log_type, logs, user_id)
        redirect_url = url_for('lt.log_form', log_type=log_type)
        redirect_url += "?u=" + user_id
        return redirect(redirect_url)
    return "Log type not found", 404


@lt_bp.route('/lt/<log_type>/delete/<int:log_id>', methods=['GET'])
def delete_log(log_type, log_id):
    if log_type in config['log_types']:
        user_id = request.args.get('u', '')
        logs = read_logs(log_type, user_id)

        logs = [log for log in logs if log.get('id') != log_id]

        write_logs(log_type, logs, user_id)
        redirect_url = url_for('lt.log_form', log_type=log_type)
        redirect_url += "?u=" + user_id
        return redirect(redirect_url)
    return "Log type not found", 404
