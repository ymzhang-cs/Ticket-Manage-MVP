# 路由蓝图注册入口
from flask import Blueprint

# 这里预留蓝图注册接口，后续各模块会在此注册

def register_blueprints(app):
    from .admin import admin_bp
    from .auth import auth_bp
    from .scan import scan_bp
    from .user import user_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(user_bp)
