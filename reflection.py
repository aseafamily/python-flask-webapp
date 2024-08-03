from flask import Flask, render_template, request, redirect, url_for, Blueprint
from datetime import datetime

reflection_bp = Blueprint('reflection', __name__)

@reflection_bp.route('/reflection', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        did_well = request.form['did_well']
        struggled_with = request.form['struggled_with']
        return redirect(url_for('reflection.result', did_well=did_well, struggled_with=struggled_with))
    return render_template('reflection_form.html')

@reflection_bp.route('/reflection/result')
def result():
    did_well = request.args.get('did_well')
    struggled_with = request.args.get('struggled_with')
    return f'<h1>Form Submission Result</h1><p>What I Did Well: {did_well}</p><p>What I Struggled With: {struggled_with}</p>'

@reflection_bp.route('/reflection/emily')
def emily_test():
    now = datetime.now()
    return render_template('e_test.html', current_time=now)
