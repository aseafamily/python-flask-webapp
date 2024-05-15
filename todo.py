from flask import Blueprint
from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify, abort
from db import db
from db_todo import Todo

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todo', methods=['POST', 'GET'])
def todo_index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        db.session.add(new_task)
        db.session.commit()
        return redirect('/todo')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks)


@todo_bp.route('/todo/delete/<int:id>')
def todo_delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'

@todo_bp.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def todo_update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        db.session.commit()
        return redirect('/todo')

    else:
        return render_template('todo_update.html', task=task)