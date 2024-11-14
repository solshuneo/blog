# route.py
import os
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from .db import User, db, UploadedFile
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    posts = [['post1', '../static/img/pika.jpg'], ['post2', '../static/img/pug.jpg']]
    return render_template("index.html", posts = posts)  # Chỉ cần tên tệp mà không có đường dẫn tuyệt đối


@main_bp.route('/login', methods = ['GET','POST'])
def login():
    print('login', session.get('logged_in'))
    if session.get('logged_in'):
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        usr = request.form.get('username')
        try:
            user = db.session.execute(db.select(User).filter_by(username=usr)).scalar_one()
            print("User found:", user)
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
    return render_template('/posts/firstpost.html')    