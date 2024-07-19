from flask import Blueprint
from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/tools/text-reader', methods=['POST', 'GET'])
def get_text_reader():
    if request.method == 'POST':
        text = request.form['text']
        return render_template("tools_text_reader.html", text=text)
    else:
        return render_template("tools_text_input.html")
    