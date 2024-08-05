from flask import Flask, render_template, request, redirect, url_for, Blueprint
from datetime import datetime
import json
from db_tennis import save_reflection
from urllib.parse import urlparse, parse_qs
from utils import display_reflection_impl

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
        next = ''
        referer = request.headers.get('Referer')
        if referer:
            # Parse the referer URL
            parsed_url = urlparse(referer)
            query_params = parse_qs(parsed_url.query)
            tennis_id = query_params.get('tennis_id', [''])[0]
            next = query_params.get('next', [''])[0]
        
        return redirect(url_for('reflection.result', did_well=did_well, struggled_with=struggled_with, consistency=consistency, defense=defense, attacking=attacking, opp_strengths=opp_strengths, opp_weaknesses=opp_weaknesses, overall_takeaways=overall_takeaways, tennis_id=tennis_id, next=next))
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
    if tennis_id:
        save_reflection(tennis_id, json_string)
        next = request.args.get('next')
        return redirect(next)
    else:
        output = display_reflection_impl(json_string)
        return output

@reflection_bp.route('/reflection/emily')
def emily_test():
    now = datetime.now()
    return render_template('e_test.html', current_time=now)
