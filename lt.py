from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import json
import os
from azure.storage.fileshare import ShareFileClient, ShareDirectoryClient
from flask_login import login_required
from datetime import datetime
from collections import Counter

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
        
        sorted_logs = sort_logs(log_config, logs)

        # Calculate statistics
        stats = {}
        if 'stats' in log_config:
            for stat_name, stat_config in log_config['stats'].items():
                if stat_config['function'] == 'count':
                    stats[stat_name] = len(sorted_logs)
                elif stat_config['function'] == 'sum':
                    column = stat_config['column']
                    if column and column in log_config['fields']:
                        # Sum values in the specified column
                        total = sum(float(log.get(column, 0)) for log in logs if log.get(column))
                        stats[stat_name] = total
                elif stat_config['function'] == 'average_interval':
                    column = stat_config['column']
                    if column in log_config['fields'] and log_config['fields'][column]['type'] == 'date':
                        if logs:
                            # Extract and sort dates
                            dates = sorted(datetime.strptime(log.get(column), '%Y-%m-%d') for log in logs if log.get(column))
                            if len(dates) > 1:
                                # Calculate intervals
                                intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                                # Calculate average interval
                                average_interval = int(sum(intervals) / len(intervals))
                                stats[stat_name] = average_interval
                            else:
                                stats[stat_name] = 0  # Not enough data to calculate
                elif stat_config['function'] == 'since':
                    column = stat_config['column']
                    if column in log_config['fields'] and log_config['fields'][column]['type'] == 'date':
                        if logs:
                            dates = [datetime.strptime(log.get(column), '%Y-%m-%d') for log in logs if log.get(column)]
                            if dates:
                                last_record_date = max(dates)
                                since_last_record = (datetime.now() - last_record_date).days
                                stats[stat_name] = since_last_record
                            else:
                                stats[stat_name] = None  # No dates to compare
        
        return render_template('lt_log_form.html', log_type=log_type, log_config=log_config, logs=sorted_logs, stats=stats)
    return "Log type not found", 404

@lt_bp.route('/lt/<log_type>', methods=['POST'])
def submit_log(log_type):
    if log_type in config['log_types']:
        user_id = request.args.get('u', '')
        log_data = request.form.to_dict()
        logs = read_logs(log_type, user_id)

        # Get the field types from the config
        field_types = config['log_types'][log_type].get('fields', {})

        # Convert form data based on field types
        for field, value in log_data.items():
            field_type = field_types.get(field, {}).get('type', 'text')
            if field_type == 'bool':
                log_data[field] = value == 'on'

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

        # Get the field types from the config
        field_types = config['log_types'][log_type].get('fields', {})

        # Convert form data based on field types
        for field, value in log_data.items():
            field_type = field_types.get(field, {}).get('type', 'text')
            if field_type == 'bool':
                log_data[field] = value == 'on'

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

@lt_bp.route('/lt/autocomplete/<log_type>/<field_name>', methods=['GET'])
def autocomplete(log_type, field_name):
    user_id = request.args.get('u', '')
    limit = request.args.get('limit', None)  # Get limit from query parameters if provided

    # Read logs for the given log type and user ID
    logs = read_logs(log_type, user_id)

    if field_name == '[all]':
        # Return raw log data
        # Get default sort configuration from lt_config.json
        log_config = config.get('log_types', {}).get(log_type, {})
        sorted_logs = sort_logs(log_config, logs)
        if limit:
            sorted_logs = sorted_logs[:int(limit)]
        return jsonify(sorted_logs)
    else:
        # Extract the values for the specified field and count the occurrences
        field_values = [log[field_name] for log in logs if field_name in log]
        top_values = [item for item, count in Counter(field_values).most_common(10)]
        all_values = [{'field': field_name, 'value': item} for item in top_values]
        return jsonify(all_values)
    

def sort_logs(log_config, logs):
    # Get the default sort column and order from the configuration
    sort_column = log_config.get('default_sort', {}).get('column')
    sort_order = log_config.get('default_sort', {}).get('order', 'asc')
    
    if sort_column:
        # Get the type of the sort column
        sort_column_type = log_config['fields'][sort_column]['type']
        
        # Define a sorting key function based on the field type
        def sort_key(log):
            value = log.get(sort_column)
            if sort_column_type == 'date':
                # Define the date format (update this format according to your date string format)
                date_format = "%Y-%m-%d"  # Example: "2023-08-04"
                return datetime.strptime(value, date_format) if value else datetime.min
            elif sort_column_type == 'number':
                return float(value) if value else float('-inf')
            elif sort_column_type == 'text':
                return value.lower() if value else ''
            elif sort_column_type == 'bool':
                return value if value else False
            else:
                return value
        
        # Sort logs by the specified column in the specified order
        sorted_logs = sorted(logs, key=sort_key, reverse=(sort_order == 'desc'))
    else:
        sorted_logs = logs

    return sorted_logs
