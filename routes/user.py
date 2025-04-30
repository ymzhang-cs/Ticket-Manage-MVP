from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, ProfileLog
import re

user_bp = Blueprint('user', __name__, url_prefix='/user')

def validate_strong_password(password):
    """
    密码强度校验：
    - 至少8位
    - 包含大写字母、小写字母、数字和特殊字符
    """
    if len(password) < 8:
        return False, '密码长度至少8位'
    if not re.search(r'[A-Z]', password):
        return False, '密码需包含大写字母'
    if not re.search(r'[a-z]', password):
        return False, '密码需包含小写字母'
    if not re.search(r'\d', password):
        return False, '密码需包含数字'
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, '密码需包含特殊字符'
    return True, ''

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        try:
            if form_type == 'username_form':
                new_username = request.form.get('new_username')
                if not new_username or new_username.strip() == '':
                    flash('用户名不能为空')
                    return redirect(url_for('user.user_profile'))
                if new_username == current_user.username:
                    flash('新用户名与当前相同')
                    return redirect(url_for('user.user_profile'))
                if User.query.filter_by(username=new_username).first():
                    flash('该用户名已存在')
                    return redirect(url_for('user.user_profile'))
                log = ProfileLog(
                    user_id=current_user.id,
                    action_type='username_change',
                    old_value=current_user.username,
                    new_value=new_username,
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                current_user.username = new_username
                db.session.add(log)
                flash('用户名修改成功')
            elif form_type == 'password_form':
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                if not old_password or not new_password:
                    flash('请填写新旧密码')
                    return redirect(url_for('user.user_profile'))
                if not current_user.check_password(old_password):
                    flash('旧密码错误')
                    return redirect(url_for('user.user_profile'))
                valid, msg = validate_strong_password(new_password)
                if not valid:
                    flash(msg)
                    return redirect(url_for('user.user_profile'))
                log = ProfileLog(
                    user_id=current_user.id,
                    action_type='password_change',
                    old_value='',
                    new_value='********',
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                current_user.set_password(new_password)
                db.session.add(log)
                flash('密码修改成功')
            else:
                flash('未知操作类型')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('操作失败: ' + str(e))
        return redirect(url_for('user.user_profile'))
    logs = ProfileLog.query.filter_by(user_id=current_user.id).order_by(ProfileLog.timestamp.desc()).limit(10).all()
    return render_template('user_profile.html', logs=logs)

@user_bp.route('/register', methods=['POST'])
@login_required
def register():
    if current_user.role != 'admin':
        return jsonify({'error': '权限不足'}), 403
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    valid, msg = validate_strong_password(data['password'])
    if not valid:
        return jsonify({'error': msg}), 400
    user = User(username=data['username'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})
