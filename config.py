# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
        # Cấu hình thư mục lưu file upload
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)