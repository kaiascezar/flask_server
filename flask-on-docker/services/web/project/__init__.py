from flask import Flask, jsonify, request, session, current_app, g
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
api = Api(app)
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

@app.route("/login", methods=['GET'])
def login():
    if request.method == 'GET':
        users = User.query.all()
        results = [
            {
                "id": user.userid,
                "password": user.password
            } for user in users]
        
        return {"Access Token"}