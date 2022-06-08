from flask import Flask, jsonify, request, session, current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://GTN_Admin:GTNAdmin!123@db:5432/GTN_User"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

def get_user_password(userid):
    row = db.execute(text("""
        select
            userid,
            password
        from users
        """)), {'userid' : userid}.fetchone()

    return {
        'userid' : row['userid'],
        'password' : row['password']
    } if row else None


@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        credential = request.json
        userid = credential['userid']
        password = credential['password']
        user_credential = get_user_password(userid)
        
        if userid == user_credential['userid'] and password == user_credential['password']:
            userid = user_credential['userid']
            
            return jsonify({'access Token'})
            
        
        results = db.fetchone
        
        return {results}