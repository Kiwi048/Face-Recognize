# routes.py (修改后)
from flask import request, jsonify, Blueprint  # 导入 Blueprint
from extensions import db, bcrypt, jwt  # <--- 从 extensions 导入
from models import User, Face
import base64
import os
import numpy as np
from datetime import datetime, timezone
import insightface
import cv2
from flask_jwt_extended import create_access_token

# 1. 创建蓝图对象
api_bp = Blueprint('api', __name__)

# 存放 embedding 的文件夹
EMBEDDING_FOLDER = 'uploads/embeddings'
os.makedirs(EMBEDDING_FOLDER, exist_ok=True)

# 初始化 InsightFace 模型（只加载一次）
model = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
model.prepare(ctx_id=0, det_size=(640, 640))


# 2. 将路由注册到蓝图上 (用 @api_bp.route 替代 @app.route)
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(account=data['account']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity=user.user_id,
            additional_claims={
                'role': user.role,
                'name': user.name
            }
        )
        return jsonify({
            'message': '登录成功',
            'token': access_token,
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'role': user.role,
                'account': user.account
            }
        }), 200

    return jsonify({'message': '账号或密码错误'}), 401


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(account=data['account']).first():
        return jsonify({'message': '该账号已被注册'}), 409

    role = '员工'
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        name=data['name'],
        account=data['account'],
        password=hashed_password,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()

    if 'face_photo' in data and data['face_photo']:
        try:
            img_data = data['face_photo'].split(",")[1]
            img_bytes = base64.b64decode(img_data)

            np_arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                raise ValueError("无法解码图片数据")

            faces = model.get(img)
            if not faces:
                db.session.delete(new_user)
                db.session.commit()
                return jsonify({'message': '未检测到人脸，注册失败'}), 400

            embedding = faces[0].embedding
            timestamp = int(datetime.now(timezone.utc).timestamp())
            emb_filename = f"user_{new_user.user_id}_{timestamp}.npy"
            emb_path = os.path.join(EMBEDDING_FOLDER, emb_filename)
            np.save(emb_path, embedding)

            new_user.embedding_path = emb_path

            new_face = Face(
                user_id=new_user.user_id,
                embedding_path=emb_path,
                result="注册录入"
            )
            db.session.add(new_face)
            db.session.commit()
        except Exception as e:
            # 如果人脸处理失败，回滚数据库，删除刚创建的用户
            db.session.delete(new_user)
            db.session.commit()
            return jsonify({'message': f'人脸处理失败: {str(e)}'}), 400

    return jsonify({'message': '用户注册成功'}), 201
