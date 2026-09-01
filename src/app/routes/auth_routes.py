from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.app.service.auth_service import register_user, login_user, confirm_totp_setup, verify_totp_login
from src.app.exceptions import BusinessError

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            register_user(email,password)
            return redirect(url_for('auth_bp.login'))
        except BusinessError as e:
            flash(str(e))

    return render_template("register.html")

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = login_user(email,password)
            if user['totp_enabled']:
                session['pending_2fa_user_id'] = user['id']
                return redirect(url_for('auth_bp.verify_2fa'))
            else:
                return redirect(url_for('task_bp.dashboard'))
        except BusinessError as e:
            flash(str(e))

    return render_template("login.html")

@auth_bp.route('/verify_2fa', methods = ['GET', 'POST'])
def verify_2fa():
    user_id = session.get('pending_2fa_user_id')
    if not user_id:
        return redirect(url_for('auth_bp.login'))
    if request.method == 'POST':
        code = request.form['code']
        try:
            verify_totp_login(user_id,code)
            session['user_id'] = user_id
            del session['pending_2fa_user_id']
            return redirect(url_for('task_bp.dashboard'))
        except BusinessError as e:
            flash(str(e))
    return render_template("verify_2fa.html")

@auth_bp.route('/logout' , methods = ['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth_bp.login'))

