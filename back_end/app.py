# app.py (修改为工厂模式)
import os
<<<<<<< HEAD
from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt
=======
import pytz
# 导入create_engine用于数据库连接测
from sqlalchemy import create_engine
import datetime
>>>>>>> upstream/main

def create_app():
    app = Flask(__name__)
    CORS(app)

<<<<<<< HEAD
    # 从环境变量加载配置
    db_user = os.getenv('DB_USER', 'root')
    db_pass = os.getenv('DB_PASS', '')

    # 配置应用
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@localhost/face_rec'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test'
    app.config['JWT_SECRET_KEY'] = 'testtest'
=======
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '456729')
db_host = os.getenv('DB_HOST', 'localhost')


# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/face_rec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'test'  # 可以自定义，建议复杂一点
app.config['JWT_SECRET_KEY'] = 'testtest'  # 可以自定义，建议复杂一点
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 设置token不过期（开发环境）

# 创建中国时区对象（UTC+8）
SHANGHAI_TZ = pytz.timezone('Asia/Shanghai')

>>>>>>> upstream/main

    # 初始化插件
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    from routes import api_bp
    app.register_blueprint(api_bp)

<<<<<<< HEAD
    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()

    return app
=======
if __name__ == '__main__':
    # 测试数据库连接
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        print("数据库连接成功")
        connection.close()
    except Exception as e:
        print(f"数据库连接失败: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> upstream/main
