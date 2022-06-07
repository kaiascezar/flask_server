from flask import Flask, jsonify, request, session, current_app, g
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.model):
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
    
