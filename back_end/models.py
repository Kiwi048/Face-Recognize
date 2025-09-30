from extensions import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255), default='员工')
    embedding_path = db.Column(db.String(255))

    faces = db.relationship('Face', backref='user', cascade="all, delete-orphan")
    attendances = db.relationship('Attendance', backref='user', cascade="all, delete-orphan")

class Face(db.Model):
    __tablename__ = 'face'
    rec_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    embedding_path = db.Column(db.String(255))
    rec_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    result = db.Column(db.String(255))

class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    clock_in_time = db.Column(db.DateTime)
    clock_out_time = db.Column(db.DateTime)
    clock_in_status = db.Column(db.String(20), default='正常')
    clock_out_status = db.Column(db.String(20), default='正常')
