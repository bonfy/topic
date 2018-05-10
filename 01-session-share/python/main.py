# -*- coding:utf-8 -*-
###
# Author: bonfy
# Email: foreverbonfy@163.com
###
from flask import Flask, session, jsonify, request, make_response
import jwt
import functools
import datetime
import time

HEADER_TOKEN = 'X-ACCESS-TOKEN'
API_TOKEN = 'API-TOKEN'
SECRET_KEY = 'secret_key'
COOKIE_EXPIRE_DAYS = 1
app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_expire_date(days=COOKIE_EXPIRE_DAYS):
    now_date = datetime.datetime.now()
    expire_date = now_date + datetime.timedelta(days=days)
    return expire_date


def generate_token(username):
    expire_date = get_expire_date()
    token = jwt.encode({'user': username, 'exp': expire_date}, SECRET_KEY)
    return token


def login_required(f):

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return 'need login'

        return f(*args, **kwargs)

    return decorated_function


def jwt_token_required(f):

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        api_token = 'api_token'
        if API_TOKEN in request.headers and request.headers[
            API_TOKEN
        ] == api_token:
            return f(*args, **kwargs)

        if HEADER_TOKEN in request.headers:
            token = request.headers[HEADER_TOKEN]
        if not token:
            return jsonify(
                {'status': 'error', 'result': 'Token is missing!'}
            ), 401

        try:
            data = jwt.decode(token, SECRET_KEY)
            user = data.get('user')
        # print(f'{user} ACCESS API')
        # TODO: vierify user in redis
        except Exception as e:
            # print('Exception: ', e)
            return jsonify(
                {'status': 'error', 'result': 'Token is invalid'}
            ), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def home():
    return 'hello'


@app.route('/login')
def login():
    username = 'bonfy'
    token = generate_token(username)
    session['username'] = username
    session['token'] = token
    # Set cookie
    response = make_response('login finish')
    # expires 60 seconds
    response.set_cookie(
        'token', token, expires=time.time() + COOKIE_EXPIRE_DAYS * 24 * 60 * 60
    )
    return response


@app.route('/logout')
def logout():
    session.clear()
    print(session)
    response = make_response('logout out')
    response.set_cookie('name', '', expires=0)
    return response


@app.route('/secure')
@login_required
def secure():
    return 'secure thing'


@app.route('/jwt')
@jwt_token_required
def jwt_token():
    return 'jwt ok'
