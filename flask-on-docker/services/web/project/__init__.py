import jwt
import bcrypt

from flask      import Flask, request, jsonify, current_app, Response, g
from sqlalchemy import create_engine, text
from datetime   import datetime, timedelta
from functools  import wraps

def get_user(user_id):
    user = current_app.database.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id' : user_id 
    }).fetchone()

    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None

def insert_user(user):
    return current_app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """), user).lastrowid

def get_user_id_and_password(email):
    row = current_app.database.execute(text("""    
        SELECT
            id,
            hashed_password
        FROM users
        WHERE email = :email
    """), {'email' : email}).fetchone()

    return {
        'id'              : row['id'],
        'hashed_password' : row['hashed_password']
    } if row else None

#########################################################
#       Decorators
#########################################################
def login_required(f):      
    @wraps(f)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization') 
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256') 
            except jwt.InvalidTokenError:
                 payload = None     

            if payload is None: return Response(status=401)  

            user_id   = payload['user_id']  
            g.user_id = user_id
            g.user    = get_user(user_id) if user_id else None
        else:
            return Response(status = 401)  

        return f(*args, **kwargs)
    return decorated_function

def create_app(test_config = None):
    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database     = create_engine(app.config.from_object("project.config.Config"))
    app.database = database

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )

        new_user_id = insert_user(new_user)
        new_user    = get_user(new_user_id)

        return jsonify(new_user)
        
    @app.route('/login', methods=['POST'])
    def login():
        credential      = request.json
        email           = credential['email']
        password        = credential['password']
        user_credential = get_user_id_and_password(email)

        if user_credential and bcrypt.checkpw(password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8')): 
            user_id = user_credential['id'] 
            payload = {     
                'user_id' : user_id,
                'exp'     : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
            }
            token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], 'HS256') 

            return jsonify({        
                'access_token' : token.decode('UTF-8')
            })
        else:
            return '', 401