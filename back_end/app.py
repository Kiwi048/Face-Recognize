# app.py (修改为工厂模式)
import os
from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 从环境变量加载配置
    db_user = os.getenv('DB_USER', 'root')
    db_pass = os.getenv('DB_PASS', '')

    # 配置应用
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@localhost/face_rec'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test'
    app.config['JWT_SECRET_KEY'] = 'testtest'

    # 初始化插件
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    from routes import api_bp
    app.register_blueprint(api_bp)

    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()

    return app
