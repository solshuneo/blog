from flask import Flask, render_template, SQLAlchemy

app = Flask(__name__)
app.secret_key = "docacbanbietduocday"

db = SQLAlchemy(app)

@app.route("/")
def home():
    posts = [['post1', '../static/img/pika.jpg'], ['post2', '../static/img/pug.jpg']]
    return render_template("index.html", posts = posts)  # Chỉ cần tên tệp mà không có đường dẫn tuyệt đối


if __name__ == "__main__":
    app.run(debug=True)  # Bật chế độ debug để dễ dàng phát hiện lỗi
