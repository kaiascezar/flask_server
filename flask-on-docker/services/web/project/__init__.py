from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
      
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/')
def hello_world():
    return jsonify(hello="world")