from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route("/login", methods=['POST'])
def login():
    userinfo = request.json
    userid = userinfo['name']
    password = userinfo['password']
    user = User.query.filter(user.name == userid).first
    if user.name == userid and user.password == password:
        return jsonify("Token")