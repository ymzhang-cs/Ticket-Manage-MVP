from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # admin/checker

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    note = db.Column(db.String(100))
    scanned = db.Column(db.Boolean, default=False)

class ScanLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
    checker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    code = db.relationship('Code', backref='logs')
    checker = db.relationship('User', backref='scan_logs')
    
class ProfileLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action_type = db.Column(db.String(50))  # 'username_change' / 'password_change'
    old_value = db.Column(db.String(200))
    new_value = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))   # 存储客户端IP
    user_agent = db.Column(db.Text)         # 存储浏览器User-Agent
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProfileLog {self.action_type} at {self.timestamp}>'

class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # 独立于User外键（避免用户删除后关联失效）
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # 支持IPv6
    user_agent = db.Column(db.Text)
    success = db.Column(db.Boolean)  # 登录成功与否
    
    def __repr__(self):
        return f'<LoginLog {self.username} {"成功" if self.success else "失败"}>'
