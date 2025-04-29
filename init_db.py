from app import app
from models import db, User

with app.app_context():
    db.create_all()
    # 创建初始管理员
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
    print("数据库初始化完成")