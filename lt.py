from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import json
import os

lt_bp = Blueprint('lt', __name__)

# Load configuration file
with open('lt_config.json', 'r') as f:
    config = json.load(f)

def read_logs(log_type):
    filename = f"{log_type}_logs.json"
    logs = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            logs = [json.loads(line) for line in f]
    return logs

def write_logs(log_type, logs):
    filename = f"{log_type}_logs.json"
    with open(filename, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')

@lt_bp.route('/lt')
def index():
    log_types = config['log_types']
    return render_template('lt_index.html', log_types=log_types)

@lt_bp.route('/lt/<log_type>', methods=['GET'])
def log_form(log_type):
    if log_type in config['log_types']:
        log_config = config['log_types'][log_type]
        logs = read_logs(log_type)
        return render_template('lt_log_form.html', log_type=log_type, log_config=log_config, logs=logs)
    return "Log type not found", 404

@lt_bp.route('/lt/<log_type>', methods=['POST'])
def submit_log(log_type):
    if log_type in config['log_types']:
        log_data = request.form.to_dict()
        logs = read_logs(log_type)

        # Add a new ID to the log data
        new_id = max([log.get('id', 0) for log in logs], default=0) + 1
        log_data['id'] = new_id

        logs.append(log_data)
        write_logs(log_type, logs)
        return redirect(url_for('lt.log_form', log_type=log_type))
    return "Log type not found", 404

@lt_bp.route('/lt/update/<log_type>/<int:log_id>', methods=['GET'])
def update_form(log_type, log_id):
    if log_type in config['log_types']:
        log_config = config['log_types'][log_type]
        filename = f"{log_type}_logs.json"
        try:
            with open(filename, 'r') as f:
                logs = [json.loads(line) for line in f]
        except FileNotFoundError:
            logs = []

        log = next((entry for entry in logs if int(entry.get('id', 0)) == log_id), None)
        if log:
            return render_template('lt_update_form.html', log_type=log_type, log_config=log_config, log=log, log_id=log_id)
        return "Log entry not found", 404
    return "Log type not found", 404

@lt_bp.route('/lt/update/<log_type>/<int:log_id>', methods=['POST'])
def update_log(log_type, log_id):
    if log_type in config['log_types']:
        log_data = request.form.to_dict()
        log_data["id"] = log_id
        filename = f"{log_type}_logs.json"
        try:
            with open(filename, 'r') as f:
                logs = [json.loads(line) for line in f]
        except FileNotFoundError:
            logs = []

        logs = [log_data if int(log.get('id', 0)) == log_id else log for log in logs]
        with open(filename, 'w') as f:
            for log in logs:
                f.write(json.dumps(log) + '\n')
        return redirect(url_for('lt.log_form', log_type=log_type))
    return "Log type not found", 404


@lt_bp.route('/lt/<log_type>/delete/<int:log_id>', methods=['GET'])
def delete_log(log_type, log_id):
    if log_type in config['log_types']:
        logs = read_logs(log_type)

        logs = [log for log in logs if log.get('id') != log_id]

        write_logs(log_type, logs)
        return redirect(url_for('lt.log_form', log_type=log_type))
    return "Log type not found", 404
