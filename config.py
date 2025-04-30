import os

# 优先使用环境变量 DATA_DIR，否则默认项目根目录下的 data 文件夹
data_dir = os.environ.get('DATA_DIR') or os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)  # 自动创建目录（如不存在）

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_dir, 'tickets.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(data_dir, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)