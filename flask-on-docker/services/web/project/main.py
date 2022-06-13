from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, text
from datetime import datetime, timedelta
from project.detectionwork import GtnOcr, PreProcessing
import bcrypt
import jwt
import hashlib


app = Flask(__name__)
token_secretkey = 'SECRET_KEY'
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(32), unique=True, nullable=False)
    pw = db.Column(db.String(250), nullable=False)
#    decrypt = db.Column(db.String(250), nullable=False)

#     def __init__(self, id, pw):
#         self.id = id
#         self.pw = pw
        
# def insert_user(id):
#     return db.session.execute(text("""
#         INSERT INTO users(
#             id,
#             pw
#         ) VALUES(
#             :id,
#             :pw
#         )
#         """), id).lastrowid 

# def get_user(index):
#     user = db.session.execute(text("""
#         SELECT
#             index,
#             id,
#             pw
#         FROM users
#         WHERE index = :index
#         """), {
#             'index' : index
#         }).fetchone()
    
#     return {
#         'index' : user['index'],
#         'id' : user['id']
#     } if user else None

       
# def get_user_id_password(id):
#     row = db.session.execute(text("""
#         SELECT
#         index,
#         pw
#         FROM id
#         WHERE id = :id
#     """), {'id' : id}).fetchone()
    
    
#     return{
#         'index' : row['index'],
#         'pw' : row['pw']
#     } if row else None

        

@app.route('/register', methods=['POST'])
def register():
    new_user = request.form.to_dict()
    id = new_user['id']
    pw = new_user['pw']
    
    pw_hash = bcrypt.hashpw(pw.encode('UTF-8'),
                            bcrypt.gensalt()
                            )
    
    db.session.add(User(id=id, pw=pw_hash))
    db.session.commit()
    
    

@app.route("/login", methods=['POST'])
def login():
    auth = request.form
    id = auth['id']
    pw = auth['pw']
    
    
    user_auth = User.query.filter((User.id == id)).first()
    password_check = bcrypt.checkpw(pw.encode('UTF-8'), User.pw.encode('UTF-8'))
     
    if user_auth and password_check:
        user_id = user_auth['index']
        payload = {
            'index' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        token = jwt.encode(payload, token_secretkey, 'HS256')
#    if id == "msg7883" and pw == "test1234!": #id pw 하드코딩
        return jsonify({
            "result": 1,
            "access_token": token
            })
    else:
        return jsonify({
            "result": 0,
            "msg": "계정 정보가 일치하지 않습니다."
        })


    
    
@app.route('/decryption', methods=['POST', 'GET'])
def get_key():
    pass
    auth_token = request.form()
    # 인증 성공 - 토큰 일치
    if auth_token['access_token'] == "token":
        return jsonify({
            "result": 1,
            "decry_key": 'kkkkkkkkkkkkkkkk',
            "iv" : "iviviviviviviviv"
        })
    # 인증 실패 - 토큰 불일치
    else:
        return {
            "result": 0,
            "msg": "권한이 없는 요청입니다."
        }, 401


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
            jumin_cnt = 0
            license_cnt = 0

            parsed = GtnOcr.reader.readtext(file.read())
            contents = list(GtnOcr.get_coordinate(parsed, tag, coordinate, verif_idcard, verif_license, verif_regist, jumin_cnt, license_cnt))
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

