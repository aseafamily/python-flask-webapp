from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import json
import os

stringing_bp = Blueprint('stringing', __name__)

# Load JSON data
def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

# Save JSON data
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

@stringing_bp.route('/stringing')
def index():
    data = load_data()
    return render_template('stringing_index.html', rackets=data['rackets'], strings=data['strings'])

@stringing_bp.route('/stringing/racket/<int:racket_id>')
def racket_view(racket_id):
    data = load_data()
    racket = next((r for r in data['rackets'] if r['id'] == racket_id), None)
    stringing_history = [s for s in data['stringing_history'] if s['racket_id'] == racket_id]
    strings = {s['id']: s for s in data['strings']}
    if racket:
        return render_template('stringing_racket.html', racket=racket, stringing_history=stringing_history, strings=strings)
    else:
        return "Racket not found", 404

@stringing_bp.route('/stringing/stringing-history')
def stringing_history():
    data = load_data()
    history = data['stringing_history']
    strings = {s['id']: s for s in data['strings']}
    return render_template('stringing_stringing_history.html', history=history, strings=strings)

@stringing_bp.route('/stringing/add-racket', methods=['GET', 'POST'])
def add_racket():
    if request.method == 'POST':
        new_racket = request.form.to_dict()
        data = load_data()
        new_racket['id'] = len(data['rackets']) + 1
        data['rackets'].append(new_racket)
        save_data(data)
        return redirect(url_for('stringing.index'))
    return render_template('stringing_add_racket.html')

@stringing_bp.route('/stringing/add-stringing/<int:racket_id>', methods=['GET', 'POST'])
def add_stringing(racket_id):
    if request.method == 'POST':
        new_stringing = request.form.to_dict()
        data = load_data()
        new_stringing['id'] = len(data['stringing_history']) + 1
        new_stringing['racket_id'] = racket_id
        data['stringing_history'].append(new_stringing)
        save_data(data)
        return redirect(url_for('stringing.racket_view', racket_id=racket_id))
    data = load_data()
    strings = data['strings']
    return render_template('stringing_add_stringing.html', racket_id=racket_id, strings=strings)

@stringing_bp.route('/stringing/add-string', methods=['GET', 'POST'])
def add_string():
    if request.method == 'POST':
        new_string = request.form.to_dict()
        data = load_data()
        new_string['id'] = len(data['strings']) + 1
        data['strings'].append(new_string)
        save_data(data)
        return redirect(url_for('stringing.index'))
    return render_template('stringing_add_string.html')
