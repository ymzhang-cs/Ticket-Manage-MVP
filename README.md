# Flask 票务管理系统

## Docker 构建

使用 Docker 构建和运行 Flask 票务管理系统。可选，也可以使用 Docker Hub 上的镜像。

```shell
docker build -t ymzhangcs/ticket-manage:latest .
```

## 部署（Docker Compose）

确保已安装 Docker 和 Docker Compose。

文件结构如下（已经在仓库的 deploy 文件夹下），按需替换 `[域名]` 和 `[邮箱]`：

```
deploy/
├── docker-compose.yml
└── nginx/
    └── nginx.conf
```

在 `deploy` 文件夹下，运行以下命令获取证书（只需要运行一次）：

```shell
docker-compose run --rm certbot
```

然后，运行以下命令启动应用和 Nginx：

```shell
docker-compose up -d
```

## 前端页面组织

所有前端页面位于 `templates/` 目录，采用 Flask + Jinja2 模板渲染，主要页面包括：

- `login.html`：登录页
- `admin_dashboard.html`：管理员仪表盘，展示统计数据和最新检票记录
- `admin_codes.html`：票务数据管理（增删改查、导入导出、二维码生码等）
- `admin_users.html`：用户管理（添加、删除、角色分配）
- `admin_login_logs.html`：登录日志查询
- `scanner.html`：检票员扫码检票页面，支持实时扫码、结果提示音、历史记录
- `user_profile.html`：用户个人资料页，支持用户名/密码修改及操作日志
- `base.html`：基础模板，包含导航栏、消息提示等

页面风格基于 Bootstrap，扫码功能依赖 `html5-qrcode` 前端库。

## 后端接口

后端采用 Flask 框架，接口分为多个蓝图（Blueprint）：

- `auth`：认证相关（登录、登出）
- `admin`：管理员相关（票务、用户、日志管理等）
- `scan`：扫码检票接口（二维码验证、扫码页面）
- `user`：用户个人资料与操作

主要接口示例：

- `/login`：登录表单提交
- `/admin/`：管理面板
- `/admin/codes`：票务数据管理
- `/admin/update_code/<id>`：票务状态更新（POST，AJAX）
- `/admin/delete_code/<id>`：票务删除（POST，AJAX）
- `/admin/import`：票务Excel导入
- `/admin/qrcode/<code>`：生成二维码图片
- `/scan/`：扫码检票页面
- `/scan`（POST）：扫码验证接口（返回票务信息/状态）
- `/user/profile`：个人资料页（用户名/密码修改）

## 数据库结构

数据库采用 SQLite，ORM 使用 SQLAlchemy，主要表结构如下：

- `User`：用户表（id, username, password_hash, role）
- `Code`：票务表（id, code, name, phone, note, scanned）
- `ScanLog`：检票日志（id, code_id, checker_id, timestamp）
- `ProfileLog`：用户操作日志（id, user_id, action_type, old_value, new_value, ip_address, user_agent, timestamp）
- `LoginLog`：登录日志（id, username, success, ip_address, user_agent, timestamp）

各表通过外键关联，支持用户、票务、日志等多维度管理。
