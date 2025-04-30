# 使用官方 Python 镜像（推荐 slim 版本精简体积）
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露 Flask 默认端口
EXPOSE 8080

# 容器启动命令（运行 app.py）
CMD ["python", "app.py"]