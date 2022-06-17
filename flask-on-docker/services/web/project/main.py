from flask import Flask, jsonify, request, Response, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, text
from datetime import datetime, timedelta
from project.detectionwork import GtnOcr, PreProcessing
import bcrypt
import jwt
import hashlib
from functools import wraps
import secrets

app = Flask(__name__)
token_secretkey = 'SECRET_KEY'
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

# DB Data
class User(db.Model):
    __tablename__ = "users"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(32), unique=True, nullable=False)
    pw = db.Column(db.String(250), nullable=False)
    # key = db.Column(db.String(250), nullable=True)
    # iv = db.Column(db.String(250), nullable=True)


def get_user(user_id):
    user = db.session.execute(text("""
        SELECT
        index,
        id,
        pw
        FROM users
        WHERE index = :user_id
    """), {
        'user_id' : user_id
    }).fetchone()

    return {
        'index' : user['index']
    } if user else None



# DB에서 id/pw 추출하는 메서드       
def get_user_id_password(id):
    row = db.session.execute(text("""
        SELECT
        index,
        pw
        FROM users
        WHERE id = :id
    """), {'id' : id}).fetchone()
    
    
    return{
        'index' : row['index'],
        'pw' : row['pw']
    } if row else None


# key값 호출하는 메서드
def get_key_iv(id):
    row = db.session.execute(text("""
        SELECT
        key,
        iv
        FROM users
        WHERE id = :id
    """), {'id' : id}).fetchone()

    return{
        'key' : row['key'],
        'iv' : row['iv']
    } if row else None

# def login_required(f):
    # @wraps(f)
    # def decorated_function(*args, **kwargs):
        # access_token = request.headers.get('Authorization')
        # if access_token is not None:
            # try:
                # payload = jwt.decode(access_token, token_secretkey, 'HS256')
            # except jwt.InvalidTokenError:
                # payload = None
# 
            # if payload is None: return Response(status=401)
# 
            # user_id = payload['user_id']
            # g.user_id = user_id
            # g.user = get_user(user_id) if user_id else None
        # else:
            # return Response(status = 401)
# 
        # return f(*args, **kwargs)
    # return decorated_function



@app.route('/register', methods=['POST'])
def register():
    new_user = request.form.to_dict()
    id = new_user['id']
    pw = new_user['pw']

    pw_hash = bcrypt.hashpw(pw.encode('UTF-8'),
                            bcrypt.gensalt()
                            ).decode('utf-8')
    
    # db.session.add(User(id = id, pw = pw_hash, key = key, iv = iv))
    db.session.add(User(id = id, pw = pw_hash))
    db.session.commit()
    
    return jsonify('Welcome' + ' ' + id)
    
    

@app.route("/login", methods=['POST'])
def login():
    auth = request.form
    id = auth['id']
    pw = auth['pw']
    user_auth = get_user_id_password(id)
    
    # 계정 정보(id, pw)를 DB와 비교
    if user_auth and bcrypt.checkpw(pw.encode('utf-8'), user_auth['pw'].encode('UTF-8')):
        user_id = user_auth['index']
        payload = {
            'index' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        # TO-DO : 이하 3개를 DB에 암호화 하여 저장
        token = jwt.encode(payload, token_secretkey, 'HS256')
        
        # key = get_key_iv(id)

        return jsonify({
            "result": 1,
            "access_token": token
            # "key" : key['key'],
            # "iv" : key['iv']
            })
    else:
        return jsonify({
            "result": 0,
            "msg": "계정 정보가 일치하지 않습니다."
        })

    
@app.route('/decryption', methods=['POST', 'GET'])
#@login_required
def get_key():
    auth_token = request.form
    # 인증 성공 - 토큰 일치
    # TO-DO: if auth_token['access_token'] == 'DB에서 불러온 token'
    token = jwt.decode(auth_token['access_token'],token_secretkey, 'HS256')
    
    
    if token['index'] == get_user(int(token['index'])):
        # key = secrets.token_hex(8)            # 암/복호화 키
        # iv = secrets.token_hex(8)             # 초기화 벡터
        return jsonify({
            "result": 1,
            "key": "ABCDEFGH12345678",
            "iv" : "1234567812345678"
        })
    # 인증 실패 - 토큰 불일치
    else:
        return jsonify({
            "result": 0,
            "msg": "권한이 없는 요청입니다.",
            "token": token,
            "auth_token": auth_token
        }), 401


@app.route('/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        # 파일이 첨부되어 있는가 확인
        if 'file' not in request.files:
            return jsonify({
                "result": 0,
                "msg": "파일이 없습니다."
            })

        file = request.files['file']

        if file and GtnOcr.allowed_file(file.filename):
            # 검증에 필요한 자료구조 및 변수
            tag = str()
            coordinate = list()
            verif_idcard = list(0 for i in range(0, 5))
            verif_license = list(0 for i in range(0, 5))
            verif_regist = list(0 for i in range(0, 9))
            priv_cnt = 0

            parsed = GtnOcr.reader.readtext(file.read())
            contents = list(GtnOcr.get_coordinate(parsed, tag, coordinate, verif_idcard, verif_license, verif_regist, priv_cnt))
            # 개인정보 탐지 내용이 없을 경우
            if contents[1] == []:
                return jsonify({
                    "result": 0,
                    "msg": "No Contents",
                    "tag": "",
                    "count": 0,
                    "data": []
                })
            # 개인정보 탐지 내용이 있을 경우
            else:
                return jsonify({
                    "result": 1,
                    "msg": "",
                    "tag": contents[0],
                    "count": contents[2],
                    "data": contents[1]
                })
        # 파일 형식이 허용되지 않을 경우
        else:
            return jsonify({
                "result": 0,
                "msg": "허용되지 않는 파일 형식입니다."
            }), 403
    # POST 의외의 접근 방식 방지
    else:
        return jsonify({
            "result": 0,
            "msg": "허용되지 않은 접근입니다."
        }), 403

