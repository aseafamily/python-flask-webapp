from flask import Flask, render_template, request, redirect, url_for, Blueprint
from datetime import datetime
import json
from db_tennis import save_reflection, get_reflection
from urllib.parse import urlparse, parse_qs
from utils import display_reflection_impl
import markdown2

reflection_bp = Blueprint('reflection', __name__)

@reflection_bp.route('/reflection', methods=['GET', 'POST'])
def form():
    category = request.args.get('category')
    if category:
        category = category.strip()
    is_new = request.args.get('is_new', 'False').lower() == 'true'
    tennis_id = request.args.get('tennis_id') 

    consistency = 0
    defense = 0
    attacking = 0
    intensity = 0
    initial_content = ''

    if is_new:
        if category == 'Match' or category == 'Play':
            initial_content = '''
### Did Well:
-  

### Struggled With:
- 

### Opponent Strengths:
- 

### Opponent Weaknesses:
- 

### Overall Takeaways:
- 

'''
        elif category == 'Group' or category == 'Private' or category == 'Semi' or category == 'Fitness':
            initial_content = '''
### Learned and practiced:
- 

### What will I practice after learned:
- 

'''
        elif category == 'Practice':
            initial_content = '''
### Improved On: 
-  

### Need to Work On: 
- 

### Overall Takeaways: 
- 

'''
        elif category == 'Coach':
            initial_content = '''
### Skills Focused On:
- 

### Player Progress:
- 

### Areas for Improvement:
- 

### Coaching Adjustments:
- 

### Next Steps:
- 
'''
    else:
        # retrive content from database
        if tennis_id:
            reflection = get_reflection(tennis_id)
            data = json.loads(reflection)
            consistency = data.get('consistency')
            defense = data.get('defense')
            attacking = data.get('attacking')
            intensity = data.get('intensity')
            initial_content = data.get('content')

    if request.method == 'POST':
        content = request.form['content']
        consistency = request.form['consistency']
        defense = request.form['defense']
        attacking = request.form['attacking']
        intensity = request.form['intensity']
        

        tennis_id = ''
        next = ''
        referer = request.headers.get('Referer')
        if referer:
            # Parse the referer URL
            parsed_url = urlparse(referer)
            query_params = parse_qs(parsed_url.query)
            tennis_id = query_params.get('tennis_id', [''])[0]
            next = query_params.get('next', [''])[0]
        return redirect(url_for('reflection.result', consistency=consistency, defense=defense, attacking=attacking, intensity=intensity, content=content, tennis_id=tennis_id, next=next))
    
    return render_template('reflection_form.html', initial_content=initial_content, category=category, tennis_id=tennis_id, consistency=consistency, defense=defense, attacking=attacking, intensity=intensity)

@reflection_bp.route('/reflection/result')
def result():
    tennis_id = request.args.get('tennis_id')
    consistency = request.args.get('consistency')
    defense = request.args.get('defense')
    attacking = request.args.get('attacking')
    intensity = request.args.get('intensity')
    content = request.args.get('content')
    
    data = {
        "consistency": consistency,
        "defense": defense,
        "attacking": attacking,
        "intensity": intensity,
        "content": content,
    }
    json_string = json.dumps(data)

    if tennis_id:
        save_reflection(tennis_id, json_string)
        next = request.args.get('next')
        return redirect(next)
    else:
        ratings_html = f"""
        <h3>Player Ratings</h3>
        <ul>
            <li><strong>Consistency:</strong> {consistency}</li>
            <li><strong>Defense:</strong> {defense}</li>
            <li><strong>Attacking:</strong> {attacking}</li>
            <li><strong>Intensity:</strong> {intensity}</li>
        </ul>
        """
        #output = display_reflection_impl(json_string)
        html_content = markdown2.markdown(content)
        full_html_content = html_content + ratings_html
        return full_html_content

@reflection_bp.route('/reflection/emily')
def emily_test():
    now = datetime.now()
    return render_template('e_test.html', current_time=now)
