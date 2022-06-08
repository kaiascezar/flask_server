from flask import Flask, url_for, render_template
from flask import request, redirect, session
from flask_sqlalchemy import SQLAlchemy
#from service import blogopen



app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

api = Api(app)
db = SQLAlchemy(app)
#cur = db.cursor()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


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

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				return 'Dont Login'
		except:
			return "Dont Login"