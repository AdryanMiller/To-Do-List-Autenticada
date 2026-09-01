from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.app.service.task_service import create_task, list_tasks, update_task, update_task_status, delete_task
from src.app.routes.decorators import login_required
from src.app.exceptions import BusinessError

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/list_task', methods=['GET'])
@login_required
def list_task_routes():
    try:
        user_id = session.get('user_id')
        filter_task = request.args.get('filter_task','all')
        tasks = list_tasks(user_id, filter_task)
        return render_template("task_bp.html", list=tasks)
    except BusinessError as e:
        flash(str(e))
        return render_template("task_bp.html", list=[])

@task_bp.route('/create_task', methods=['POST'])
@login_required
def create_task_route():
    try:
        user_id = session.get('user_id')
        task_title = request.form.get('task_title')
        task_description = request.form.get('task_description')
        create_task(user_id, task_title, task_description)
        return redirect(url_for('task_bp.list_task_routes'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('task_bp.list_task_routes'))

@task_bp.route('/task/<int:task_id>/edit', methods=['POST'])
@login_required
def edit_task_route(task_id:int):
    try:
        user_id = session.get('user_id')
        task_title = request.form.get('task_title')
        task_description = request.form.get('task_description')
        update_task(user_id, task_id, task_title, task_description)
        return redirect(url_for('task_bp.list_task_routes'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('task_bp.list_task_routes'))

@task_bp.route('/task/<int:task_id>/status', methods=['POST'])
@login_required
def edit_task_status(task_id:int):
    try:
        user_id = session.get('user_id')
        task_status = request.form.get('task_status')
        update_task_status(user_id, task_id, task_status)
        return redirect(url_for('task_bp.list_task_routes'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('task_bp.list_task_routes'))

@task_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task_route(task_id:int):
    try:
        user_id = session.get('user_id')
        delete_task(user_id, task_id)
        return redirect(url_for('task_bp.list_task_routes'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('task_bp.list_task_routes'))

