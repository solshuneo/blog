# route.py
import os
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from .db import User, db, UploadedFile, Post
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
    posts = Post.query.all()
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
    posts = Post.query.all()
    return render_template('admin.html', users=users, posts = posts)     
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
import os
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Đường dẫn thư mục upload chung
UPLOAD_FOLDER = 'uploads'

from flask import render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Đảm bảo rằng các thư viện của bạn đã được import đúng
UPLOAD_FOLDER_TEMPLATE = 'templates/uploads'  # Đường dẫn đến thư mục uploads
UPLOAD_FOLDER_STATIC = 'static/uploads'  # Đường dẫn đến thư mục uploads
@main_bp.route('/upload', methods=['POST'])
def upload_post():
    # Kiểm tra xem người dùng đã đăng nhập chưa (giả sử bạn có cơ chế đăng nhập)
    if session.get('username') is None:
        return render_template('404.html')
    
    username = session.get('username')
    user = User.query.filter_by(username=username).first()  # Tìm người dùng theo username

    # Kiểm tra các tệp có được gửi lên không
    if 'thumbnail' not in request.files or 'post_file' not in request.files or 'css_file' not in request.files or 'js_file' not in request.files:
        flash('Missing file(s). Please upload all required files.', 'error')
        return render_template('404.html')

    # Lấy các tệp từ request
    thumbnail = request.files['thumbnail']
    post_file = request.files['post_file']
    css_file = request.files['css_file']
    js_file = request.files['js_file']
    
    # Kiểm tra nếu người dùng không chọn tệp
    if thumbnail.filename == '' or post_file.filename == '' or css_file.filename == '' or js_file.filename == '':
        flash('No file selected. Please select all files.', 'error')
        return render_template('404.html')

    # Lấy tiêu đề bài viết từ form
    title = request.form['title']
    print("title ne", title)
    # Tạo thư mục uploads/{username}/{title}
    user_folder_template = os.path.join(UPLOAD_FOLDER_TEMPLATE, username)
    user_folder_static = os.path.join(UPLOAD_FOLDER_STATIC, username)
    title_folder_template = os.path.join(user_folder_template, title)
    title_folder_static = os.path.join(user_folder_static, title)

    
    if os.path.exists(title_folder_template):
        flash(f'Title "{title}" already exists. Please choose another title.', 'error')
        return render_template('404.html')
    if os.path.exists(title_folder_static):
        flash(f'Title "{title}" already exists. Please choose another title.', 'error')
        return render_template('404.html')
    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(title_folder_template):
        os.makedirs(title_folder_template)
    if not os.path.exists(title_folder_static):
        os.makedirs(title_folder_static)

    # Lưu các tệp vào thư mục title
    thumbnail_path = os.path.join(title_folder_static, secure_filename(thumbnail.filename))
    post_file_path = os.path.join(title_folder_template, secure_filename(post_file.filename))
    css_file_path = os.path.join(title_folder_static, secure_filename(css_file.filename))
    js_file_path = os.path.join(title_folder_static, secure_filename(js_file.filename))

    # Lưu các tệp vào hệ thống
    thumbnail.save(thumbnail_path)
    post_file.save(post_file_path)
    css_file.save(css_file_path)
    js_file.save(js_file_path)

    # Lưu thông tin bài viết vào cơ sở dữ liệu
    # thumbnail_url = os.path.relpath(thumbnail_path, UPLOAD_FOLDER)  # Đoạn này lấy đường dẫn bắt đầu từ uploads
    # post_url = os.path.relpath(post_file_path, UPLOAD_FOLDER)
    # css_url = os.path.relpath(css_file_path, UPLOAD_FOLDER)
    # js_url = os.path.relpath(js_file_path, UPLOAD_FOLDER)
    thumbnail_url_string = "../static/" + f"uploads/{username}/{title}/{os.path.basename(thumbnail.filename)}"
    post_url_string = f"uploads/{username}/{title}/{os.path.basename(post_file.filename)}"
    css_url_string = "../static/" + f"uploads/{username}/{title}/{os.path.basename(css_file.filename)}"
    js_url_string = "../static/" + f"uploads/{username}/{title}/{os.path.basename(js_file.filename)}"
    # Lưu thông tin bài viết vào cơ sở dữ liệu
    post = Post(
        title=title,
        thumbnail_url=thumbnail_url_string,
        post_url=post_url_string,
        css_url=css_url_string,
        js_url=js_url_string,
        author_id=user.id  # ID của tác giả lấy từ thông tin người dùng
    )


    # Thêm bài viết vào cơ sở dữ liệu và commit
    db.session.add(post)
    db.session.commit()
    print(post)
    # Thông báo thành công và chuyển hướng đến bài viết
    flash('Post uploaded successfully!', 'success')
    print("post title ne1", title)

    # Tìm user theo username
    user = User.query.filter_by(username=username).first_or_404()

    # Tìm bài viết theo tiêu đề và thuộc về user đó
    post = Post.query.filter_by(title=title, author_id=user.id).first_or_404()

    # Tạo URL cho CSS thông qua url_for
    css_url = url_for('static', filename=post.css_url)

    # Chuyển hướng với URL mới
    return redirect(url_for('main.view_post', username=username, post_title=title, css_url=css_url))
    # return redirect(url_for('main.view_post', username=username, post_title=title))  # Redirect đến trang bài viết sau khi upload thành công

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

# @main_bp.route('/user/<username>/post/<string:post_title>', methods=['GET'])
# def view_post(username, post_title):
#     print("post title ne1", post_title)

#     # Tìm user theo username
#     print("call here")
#     user = User.query.filter_by(username=username).first_or_404()
#     print("call here1234")
#     print(user.id)
#     print("post title ne2", post_title)
#     # Tìm bài viết theo tiêu đề và thuộc về user đó
#     post = Post.query.filter_by(title=post_title, author_id=user.id).first_or_404()
#     print(post)
#     print("call here123")

#     # Render view_post.html với thông tin bài viết
#     # return render_template("./posts/firstpost.html")
#     print(post.css_url)
#     return render_template(post.post_url, css = post.css_url)
@main_bp.route('/user/<username>/post/<string:post_title>', methods=['GET'])
def view_post(username, post_title):
    # Lấy css_url từ query string (thông qua redirect)
    css_url = request.args.get('css_url')

    # Tìm user theo username
    user = User.query.filter_by(username=username).first_or_404()

    # Tìm bài viết theo tiêu đề và thuộc về user đó
    post = Post.query.filter_by(title=post_title, author_id=user.id).first_or_404()

    # Render view_post.html với thông tin bài viết
    return render_template(post.post_url, css=css_url)
