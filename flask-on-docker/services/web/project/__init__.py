from flask import Flask, jsonify, request, session, current_app, g
from flask.json import JSONEncoder
import psycopg2
from credentials import DATABASE as DB


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = psycopg2.connect(dbname=DB['GTN_User'],
                      user=DB['GTN_Admin'],
                      host=DB['localhost'],
                      password=DB['GTNAdmin!123'],
                      port=5432)

#cur = db.cursor()
#
#cur.execute("""CREATE TABLE users (
#                    id INT,
#                    userid TEXT,
#                    password TEXT
#            )""")

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

#def get_user_password(userid):
#    row = db.execute(text("""
#        select
#            userid,
#            password
#        from users
#        """)), {'userid' : userid}.fetchone()
#
#    return {
#        'userid' : row['userid'],
#        'password' : row['password']
#    } if row else None
    
   
     

@app.route("/login")
def login():
    users = User.query.all()
    #if request.method == 'POST':
        #request_id = request.json
        #userid = request_id['userid']
        #get_user_password(userid)
    return print(text(users))
#        credential = request.json
#        userid = credential['userid']
#        password = credential['password']
#        return db.execute(text("""
#        select
#            userid,
#            password
#        from users
#        """)), {'userid' : userid}.fetchone()
        #user_credential = get_user_password(userid)
        
#        ##if userid == user_credential['userid'] and password == user_credential['password']:
        ##    user_id = user_credential['id']
        #    
        #    return jsonify({'access Token'})
            
        
        #results = db.fetchone
        
#        return {results}
#    else:
#        return '', 401