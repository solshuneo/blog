# route.py
import os
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from .db import User, db, UploadedFile
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    logged_in = None
    if session.get('logged_in'):
        try:
            user = db.session.execute(db.select(User).filter_by(username=session.get('username'))).scalar_one()            
            logged_in = user
        except NoResultFound:
            print("No user found with username:")
        except MultipleResultsFound:
            print("Multiple users found with username:")
    posts = [['post1', '../static/img/pika.jpg'], ['post2', '../static/img/pug.jpg']]
    return render_template("index.html", posts = posts, logged_in = logged_in)


@main_bp.route('/login', methods = ['GET','POST'])
def login():
    print('login', session.get('logged_in'))
    if session.get('logged_in'):
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        usr = request.form.get('username')
        pwd = request.form.get('password')
        try:
            user = db.session.execute(db.select(User).filter_by(username=usr, password=pwd)).scalar_one()            
            session['username'] = usr
            session['logged_in'] = True
            return redirect(url_for("main.home"))
        except NoResultFound:
            print("No user found with username:")
        except MultipleResultsFound:
            print("Multiple users found with username:")
            
    return render_template("login.html")
@main_bp.route('/logout')
def logout():
    print('logout', session.get('logged_in'))
    if session.get('logged_in'):
        session.pop('logged_in')
        session.pop('username')
    return redirect(url_for("main.home"))
@main_bp.route('/admin')
def profile():
    users = User.query.all()  # Lấy toàn bộ user từ database
    return render_template('admin.html', users=users)    
@main_bp.route('/testpost', methods = ['GET', 'POST'])
def testpost():
    if 'file' in request.files:        
        file = request.files['file']
        if file.filename != '':                 
            # Lưu file vào thư mục uploads
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Lưu thông tin file vào database
            new_file = UploadedFile(filename=file.filename)
            db.session.add(new_file)
            db.session.commit()
    return render_template('/posts/firstpost.html', logged_in = None)    
@main_bp.route('/about')
def about():
    username = session.get('username')
    user = None
    if session.get('username') == username:
        user = User.query.filter_by(username=username).first()  # Tìm người dùng theo username
    return render_template('./about.html', logged_in = user)
@main_bp.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
    if session.get('username') != username:
        return render_template('404.html')
    user = User.query.filter_by(username=username).first()  # Tìm người dùng theo username
    if request.method == 'POST':
        # Lấy thông tin từ form
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        url_avatar = request.form.get('url_avatar')
        # Kiểm tra mật khẩu có khớp không
        user.url_avatar = url_avatar
        if new_password != confirm_password:
            error = "Passwords do not match."
            return render_template('user.html', logged_in=user, error=error)
        # Nếu có thay đổi mật khẩu, mã hóa mật khẩu mới và cập nhật
        if new_password:
            user.password = new_password

        # Cập nhật tên hiển thị và email
        user.display_name = display_name
        user.email = email

        # Cập nhật vào cơ sở dữ liệu
        db.session.commit()

        # Quay lại trang profile
        return redirect(url_for('main.user', username=user.username))
    if user:
        return render_template("user.html", logged_in=user)
    else:
        return "User not found", 404
