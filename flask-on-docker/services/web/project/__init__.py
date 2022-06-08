from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TEXT, INTEGER



app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

api = Api(app)
db = SQLAlchemy(app)


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

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    db.execute("select id, password from users where id='{}' and password = '{}';".format(name, password))
    result = db.fetchone
    if not result:
        return "비밀번호를 확인하세요", 400
    elif result[0] == name and result[1] == password:
        return "Access Token", 200
    
    
