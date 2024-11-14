# __init__.py

from flask import Flask
from .config import Config
from .db import db, User
from .route import main_bp
def create_app():
    print("asdfsdf")
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo database
    db.init_app(app)
    # Đăng ký blueprint cho routes
    app.register_blueprint(main_bp)
    sample_users = [
        User(type='admin', username='admin1', password='password123', display_name='Admin One', email='admin1@example.com'),
        User(type='superstaff', username='superstaff1', password='password123', display_name='Super Staff One', email='superstaff1@example.com'),
        User(type='staff', username='staff1', password='password123', display_name='Staff One', email='staff1@example.com'),
        User(type='user', username='user1', password='password123', display_name='User One', email='user1@example.com'),
        User(type='user', username='user2', password='password123', display_name='User Two', email='user2@example.com')
    ]
    print("asdfafd")
    # Thêm các user vào session và commit vào database
    with app.app_context():
        print("Creating tables and adding sample users")
        db.create_all()  # Tạo bảng nếu chưa có
        
        # Kiểm tra nếu không có user nào thì mới thêm user mẫu
        if User.query.count() == 0:
            db.session.add_all(sample_users)
            db.session.commit()  # Commit để lưu dữ liệu vào database
            print("Sample users added to database")
        else:
            print("Sample users already exist in the database")

    return app