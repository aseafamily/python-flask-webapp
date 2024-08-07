from flask import Blueprint
from flask import render_template, request
import markdown2


test_bp = Blueprint('test', __name__)

@test_bp.route('/test/markdown', methods=['GET', 'POST'])
def markdown_form():
    initial_content = "# Hello World\n\nThis is a simple **Hello World** markdown example.\n\n- Item 1\n- Item 2\n- Item 3\n\nEnjoy writing markdown with SimpleMDE!"

    if request.method == 'POST':
        content = request.form['content']
        html_content = markdown2.markdown(content)
        return render_template('test_display_markdown.html', content=html_content)
    return render_template('test_markdown.html', initial_content=initial_content)