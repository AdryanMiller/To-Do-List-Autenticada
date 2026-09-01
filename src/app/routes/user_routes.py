from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.app.service.user_service import update_avatar_service, update_password_service, get_profile_service
from src.app.service.auth_service import start_totp_setup, confirm_totp_setup
from src.app.routes.decorators import login_required
from src.app.exceptions import BusinessError

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    try:
        user_id = session.get('user_id')
        user = get_profile_service(user_id)
        return render_template('profile.html', user=user)
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('auth_bp.login'))

@user_bp.route('/profile/avatar',methods=['POST'])
@login_required
def edit_profile_avatar():
    user_id = session.get('user_id')
    avatar = request.form.get('avatar')
    try:
        update_avatar_service(user_id, avatar)
        return redirect(url_for('user_bp.profile'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('user_bp.profile'))

@user_bp.route('/profile/password', methods=['POST'])
@login_required
def edit_profile_password():
    try:
        user_id = session.get('user_id')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        update_password_service(user_id, current_password, new_password)
        return redirect(url_for('user_bp.profile'))
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('user_bp.profile'))

@user_bp.route('/profile/2fa/start', methods=['POST'])
@login_required
def start_2fa():
    try:
        user_id = session.get('user_id')
        uri_code = start_totp_setup(user_id)
        return render_template('start.html', uri_code=uri_code)
    except BusinessError as e:
        flash(str(e))
        return redirect(url_for('user_bp.profile'))

@user_bp.route('/profile/2fa/confirm', methods=['GET','POST'])
@login_required
def confirm_2fa():
    if request.method == 'POST':
        user_id = session.get('user_id')
        code = request.form.get('code')
        try:
            confirm_totp_setup(user_id, code)
            return redirect(url_for('user_bp.profile'))
        except BusinessError as e:
            flash(str(e))
    return render_template('confirm_2fa.html')

