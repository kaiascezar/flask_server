from datetime import timedelta, datetime
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import jwt



app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Unicode(256), nullable=False)
    decryptkey = db.Column(db.String(100), nullable=False)
    
    
    def __init__(self, userid, password, decryptkey):
        self.userid = userid
        self.set_password(password)
        self.decryptkey = decryptkey
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

@app.route('/')
def hello_world():
    return jsonify(hello="world")

#@app.route("/sign-up", methods=['POST'])
#def sign_up():
#    new_user = request.json
#    new_user['password'] = bcrypt.hashpw(
#        new_user['password'].encode('UTF-8'),
#        bcrypt.salt('secret')
#    )
#    
#    new_user_id = db.execute(text("""
#        INSERT INTO users(
#            user_id,
#            hashed_password,
#            decryptkey
#        ) VALUES (
#            :user_id,
#            hashed_password,
#            decryptkey
#        )    
#    """), new_user).lastrowid
#    new_user_info = get_user(new_user_id)
#    
#    return jsonify(new_user_info)

@app.route('/login', methods=['POST'])
def login():
    credential = request.json
    userid = credential['userid']
    password = credential['password']
    
    row = db.execute(text(""".
        SELECT
            id,
            password
        FROM users
        WHERE userid = :userid
    """), {'userid' : userid}).fetchone()
    
    if row and bcrypt.checkpw(password.encode('UTF-8'), row['password'].endcode('UTF-8')):
        user_id = row['userid']
        payload = {
            'user_id' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24) 
        }
        token = jwt.encode(payload, app.config['SECRET', 'HS256'])
        
        return jsonify({
            'access_token' : token.decode('UTF-8')
        })
        
    else:
        return '', 401
    