# -*- coding: utf-8 -*-
print ("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, g
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime
import os
import json
from functools import wraps
import requests

from backend import app, login_manager
from backend import manager
from backend.api_utils import *
from backend_model.database import DBManager
from backend_model.table_user import *
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(id):
    user = DBManager.db.session.query(Users).get(id)
    return user


@app.route('/api/monitor/v1/login', methods=['POST'])
def login_api():
    data = json.loads(request.data)
    result = ''

    if data['user_id'] is not None and data['user_pw'] is not None:
        print("user_id :",data['user_id'],",user_pw :",data['user_pw'])
        loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()

        if loginuser is None:
            result = {'status': False, 'reason': 1}  # ID 없음
        else:
            print("user_pw :",data["user_pw"])
            if loginuser.user_pw != password_encoder_512(data["user_pw"]):
                result = {'status': False, 'reason': 2} # PW 틀림

            else:  # Login 성공
                if loginuser.user_status == 0:
                    result = {'status': False, 'reason': 3}  # Activation 안됨
                else:
                    loginuser.last_logon_time = datetime.now()
                    loginuser.token = generate_token(data['user_id'])
                    db.session.query(Users).filter(Users.user_id == data["user_id"])\
                        .update(dict(last_logon_time=loginuser.last_logon_time, token=loginuser.token))
                    result = {'status': True, 'reason': 0, 'user': loginuser.serialize()}

    return make_response(jsonify(result), 200)

@app.route("/api/monitor/v1/logout", methods=["POST"])
def logout_api():
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    result = ''
    if token is None:
        print("token is none")
    loginUser = Users.query.filter_by(token=token).first()
    if loginUser is None:
        print("user is none")
    return make_response(jsonify(result), 200)

def generate_token(userID):
    m = hashlib.sha1()

    m.update(userID.encode('utf-8'))
    m.update(datetime.now().isoformat().encode('utf-8'))

    return m.hexdigest()

def validate_token(token):
    user = Users.query.filter_by(token=unicode(token)).first()
    ## 개발시에 주석을 풀고 자동로그인 환경 구성
    ##user = Users.query.filter_by(userID=unicode('sorang.kang@lge.com')).first()

    if user is None:
        return None
    elif user.enable_login is False:
        raise ProcessingException(description="Not Authorized", code=410)
    elif user.userType == app.config['USER_TYPE_USER']:
        manager = Users.query.filter_by(id=user.FK_manager_id).first()
        if manager is not None:
            if manager.enable_login is False:
                raise ProcessingException(description="Not Authorized", code=410)

    return user

def check_token(search_params=None, **kw):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    print("token:",token)
    user = Users.query.filter_by(token=token).first()
    if user is None:
        raise ProcessingException(description="Not Authorized", code=411)
    print("user:",user.user_id)
check_token
    #user = dict()

    #return user


def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="headers")
        token = parser.parse_args()["token"]
        print("token:", token)
        user = Users.query.filter_by(token=token).first()
        if user is None:
            raise ProcessingException(description="Not Authorized", code=411)
        print("user:", user.user_id)
        g.user = user
        return fn(*args, **kwargs)
    return decorated


def password_encoder_512(password):
    h = hashlib.sha512()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def prePasswdUpdate(input_params=None, **kw):
    if 'user_pw' in kw['data']:
        kw['data']['user_pw'] = password_encoder_512(kw['data']['user_pw'])

# manager.create_api(Users
#                    , results_per_page=10000
#                    , max_results_per_page=10000
#                    , url_prefix='/api/monitor/v1'
#                    , collection_name='users'
#                    , methods=['GET', 'DELETE', 'PATCH', 'POST']
#                    , allow_patch_many=True
#                    , preprocessors={
#                         'POST': [check_token],
#                         'PATCH_SINGLE': [check_token,prePasswdUpdate],
#                         'GET_SINGLE': [check_token],
#                         'GET_MANY': [check_token]
#                    })

def get_os_browser_from_useragent(userAgent):
    os_ver = "Unknown"
    browser_ver = "Unknown"

    if userAgent.find("Linux") != -1:
        os_ver = "Linux"
    elif userAgent.find("Mac") != -1:
        os_ver = "MacOS"
    elif userAgent.find("X11") != -1:
        os_ver = "UNIX"
    elif userAgent.find("Win") != -1:
        os_ver = "Windows"

    if userAgent.find("MSIE 6") != -1:
        browser_ver = "Internet Explorer 6"
    elif userAgent.find("MSIE 7") != -1:
        browser_ver = "Internet Explorer 7"
    elif userAgent.find("MSIE 8") != -1:
        browser_ver = "Internet Explorer 8"
    elif userAgent.find("MSIE 9") != -1:
        browser_ver = "Internet Explorer 9"
    elif userAgent.find("MSIE 10") != -1:
        browser_ver = "Internet Explorer 10"
    elif userAgent.find("Trident") != -1 or userAgent.find("trident") != -1:
        browser_ver = "Internet Explorer 11"
    elif userAgent.find("Firefox") != -1:
        browser_ver = "Firefox"
    elif userAgent.find("Opera") != -1:
        browser_ver = "Opera"
    elif userAgent.find("Chrome") != -1:
        browser_ver = "Chrome"
    elif userAgent.find("Safari") != -1 or userAgent.find("Chrome") == -1:
        browser_ver = "Safari"
    elif userAgent.find("Edge") != -1 or userAgent.find("edge") != -1:
        browser_ver = "Microsoft Edge"

    return os_ver, browser_ver


def date_encoder(thing):
    list_date = str(thing).split(":")

    if hasattr(thing, 'isoformat'):
        if len(list_date[0]) == 1:
            return "0" + thing.isoformat()
        return thing.isoformat()
    else:
        if len(list_date[0]) == 1:
            return "0" + str(thing)
        return str(thing)