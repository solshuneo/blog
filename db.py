# db.py
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
UTC_PLUS_7 = timezone(timedelta(hours=7))

# Định nghĩa bảng User
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # Quyền: admin, superstaff, staff, user
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    url_avatar = db.Column(db.String(255), nullable=True)  # Thêm trường avatar lưu URL

    def __init__(self, type, username, password, display_name, email, url_avatar=r'..\static\img\temp.jpeg'):
        self.type = type
        self.username = username
        self.password = password
        self.display_name = display_name
        self.email = email
        self.url_avatar = url_avatar  # Khởi tạo trường avatar

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)  # Tiêu đề bài viết
    thumbnail_url = db.Column(db.String(500), nullable=False)  # URL hình ảnh đại diện
    post_url = db.Column(db.String(500), nullable=False)  # URL của bài viết (.html)
    css_url = db.Column(db.String(500), nullable=True)  # URL file CSS (.css)
    js_url = db.Column(db.String(500), nullable=True)  # URL file JavaScript (.js)
    author_id = db.Column(db.Integer, nullable=False)  # ID tác giả
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC_PLUS_7), nullable=False)  # Thời gian tạo
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC_PLUS_7), 
                           onupdate=lambda: datetime.now(UTC_PLUS_7), nullable=False)  # Thời gian cập nhật

    # Quan hệ ngược với bảng User

    def __init__(self, title, thumbnail_url, post_url, author_id, css_url=None, js_url=None):
        """
        Khởi tạo một bài viết mới.
        
        Args:
            title (str): Tiêu đề bài viết.
            thumbnail_url (str): URL của ảnh đại diện.
            post_url (str): URL của bài viết.
            author_id (int): ID của tác giả.
            css_url (str, optional): URL của file CSS. Mặc định là None.
            js_url (str, optional): URL của file JavaScript. Mặc định là None.
        """
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.post_url = post_url
        self.author_id = author_id
        self.css_url = css_url
        self.js_url = js_url

    def __repr__(self):
        return (f"<Post(id={self.id}, title='{self.title}', "
                f"thumbnail_url='{self.thumbnail_url}', post_url='{self.post_url}', "
                f"css_url='{self.css_url}', js_url='{self.js_url}', "
                f"author_id={self.author_id})>")
