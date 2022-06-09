from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt


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
    
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'


@app.route("/login", methods=['POST'])
def login():
    userinfo = request.json
    userid = userinfo['name']
    password = userinfo['password']
    user = User.query.first()
    
    if user.name == userid and user.password == password:
        user_id = user.id
        payload = {
            'user_id' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        token = jwt.encode(payload, app.config['SECRET'], 'HS256')
        
        return jsonify({
            'access_token' : token
        })
    else:
        return '', 401