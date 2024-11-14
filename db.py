# db.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Định nghĩa bảng User
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # Quyền: admin, superstaff, staff, user
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, type, username, password, display_name, email):
        self.type = type
        self.username = username
        self.password = password
        self.display_name = display_name
        self.email = email
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
