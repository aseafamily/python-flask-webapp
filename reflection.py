from flask import Flask, render_template, request, redirect, url_for, Blueprint
from datetime import datetime
import json
from db_tennis import save_reflection
from urllib.parse import urlparse, parse_qs

reflection_bp = Blueprint('reflection', __name__)

@reflection_bp.route('/reflection', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        did_well = request.form['did_well']
        struggled_with = request.form['struggled_with']
        consistency = request.form['consistency']
        defense = request.form['defense']
        attacking = request.form['attacking']
        opp_strengths = request.form['opp_strengths']
        opp_weaknesses = request.form['opp_weaknesses']
        overall_takeaways = request.form['overall_takeaways']

        
        tennis_id = ''
        u = ''
        referer = request.headers.get('Referer')
        if referer:
            # Parse the referer URL
            parsed_url = urlparse(referer)
            query_params = parse_qs(parsed_url.query)
            tennis_id = query_params.get('tennis_id', [''])[0]
            u = query_params.get('u', [''])[0]
        
        return redirect(url_for('reflection.result', did_well=did_well, struggled_with=struggled_with, consistency=consistency, defense=defense, attacking=attacking, opp_strengths=opp_strengths, opp_weaknesses=opp_weaknesses, overall_takeaways=overall_takeaways, tennis_id=tennis_id, u=u))
    return render_template('reflection_form.html')

@reflection_bp.route('/reflection/result')
def result():
    did_well = request.args.get('did_well')
    struggled_with = request.args.get('struggled_with')
    tennis_id = request.args.get('tennis_id')
    consistency = request.args.get('consistency')
    defense = request.args.get('defense')
    attacking = request.args.get('attacking')
    opp_strengths = request.args.get('opp_strengths')
    opp_weaknesses = request.args.get('opp_weaknesses')
    overall_takeaways = request.args.get('overall_takeaways')
    if tennis_id:
        data = {
            "did_well": did_well,
            "struggled_with": struggled_with,
            "consistency": consistency,
            "defense": defense,
            "attacking": attacking,
            "opp_strengths": opp_strengths,
            "opp_weaknesses": opp_weaknesses,
            "overall_takeaways": overall_takeaways
        }
        json_string = json.dumps(data)
        save_reflection(tennis_id, json_string)
        player_id = request.args.get('u')
        return redirect(f"/tennis?u={player_id}")
    else:
        return f'<h1>Form Submission Result</h1><p>What I Did Well: {did_well}</p><p>What I Struggled With: {struggled_with}</p><p>Consistency: {consistency}</p><p>Defense: {defense}</p><p>Attacking: {attacking}</p><p>Opponent Strengths: {opp_strengths}</p><p>Opponent Weaknesses: {opp_weaknesses}</p><p>Overall Takeaways: {overall_takeaways}</p>'

@reflection_bp.route('/reflection/emily')
def emily_test():
    now = datetime.now()
    return render_template('e_test.html', current_time=now)
