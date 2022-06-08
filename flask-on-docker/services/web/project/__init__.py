from flask import Flask, jsonify, request, session, current_app, g
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgresql://GTN_Admin:GTNAdmin!123@db:5432/GTN_User"
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

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        users = User.query.all()
        results = [
            {
                "id": user.userid,
                "password": user.password
            } for user in users]
        
        return {results}