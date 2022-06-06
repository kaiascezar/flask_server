from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.varchar(32), unique=True, nullable=False)
    password = db.Column(db.varchar(32), nullable=False)
    decryptkey = db.Column(db.varchar(256), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    
    def __init__(self, user_id):
        self.user_id = user_id


@app.route('/')
def hello_world():
    return jsonify(hello="world")