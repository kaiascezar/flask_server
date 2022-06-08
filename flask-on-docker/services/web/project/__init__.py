from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TEXT, INTEGER



app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

api = Api(app)
db = SQLAlchemy(app)
#cur = db.cursor()

class User(db.Model):
    __tablename__ = "users"

    id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(TEXT, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)


class Check(Resource):
    def get(self):
        rows = User.query.all()
        result = [{
            'id': row.id,
            'name': row.name,
            'password': row.password
        } for row in rows]
        return result


api.add_resource(Check, '/fruit')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return '홈페이지'
    else:
        name = request.form['name']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=password).first()
            if data is not None:
                session['logged_in'] = True
                return '로그인 완료'
            else:
                return '로그인 안됨'
        except:
            return '로그인 안됨'