from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, name):
        self.name = name


@app.route("/login")
def hello_world():
    user = User.query.first()
    return jsonify('hello' + user.email)