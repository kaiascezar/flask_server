from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TEXT, INTEGER

from credentials import DATABASE as DB


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

api = Api(app)
db = SQLAlchemy(app)


class Fruit(db.Model):
    __tablename__ = "test"

    id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(TEXT)
    color = Column(TEXT)


class Check(Resource):
    def get(self):
        rows = Fruit.query.all()
        result = [{
            'id': row.id,
            'name': row.name,
            'color': row.color
        } for row in rows]
        return result


api.add_resource(Check, '/fruit')
