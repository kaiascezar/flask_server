from flask import Flask, url_for, render_template
from flask import request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

#from service import blogopen



app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

#api = Api(app)
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


#class Check(Resource):
#    def get(self):
#        rows = User.query.all()
#        result = [{
#            'id': row.id,
#            'name': row.name,
#            'password': row.password
#        } for row in rows]
#        return result
#
#
#api.add_resource(Check, '/fruit')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            print(password)
        
            db.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = db.fetchone()
            
            if account:
                password = account['password']
                print(password)
            else:
                flash('Incorrect username/password')
            
        return print('access token')