from flask import Flask, jsonify, request, session, current_app, g
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/login", methods=['GET', 'POST'])
def login():
    userid = request.json['userid']
    password = request.json['password']
    db.execute("select userid, password from users where userid='{}' and password = '{}';".format(userid, password))
    result = db.fetchone()
    if not result:
        return '해당 사용자가 존재하지 않습니다.', 400
    elif result[0] == userid and result[1] == password:
        return jsonify("access Token"), 200
