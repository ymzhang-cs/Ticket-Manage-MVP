from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User, LoginLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.record_once
def on_load(state):
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

@auth_bp.route('/')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('scan.scanner'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        log = LoginLog(
            username=username,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        if user and user.check_password(password):
            login_user(user)
            log.success = True
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('auth.index'))
        else:
            log.success = False
            db.session.add(log)
            db.session.commit()
            flash('用户名或密码错误')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('auth.login'))
