from flask import Flask, request, abort, jsonify, render_template
import jwt
import json
import hashlib
import datetime

from db_api import *

app = Flask(__name__, static_folder="../dist", template_folder="../static")

SECRET_KEY = 'my_secret_secret_key'
HASH_KEY = 'my_secret_hash_key'

def encode(string):
    return hashlib.sha1(str.encode(string)).hexdigest()

@app.route('/')
def index():
 return render_template("index.html")

@app.route('/compile', methods=['POST'])
def post_program():
    filename = request.json['filename']
    compiler_id = request.json['compiler_id']
    username = request.json['username']
    with DatabaseConnection() as dbconn:
        user_id = dbconn.get_uid_by_username(username)
    task_id = request.json['task_id']
    source = request.json['source']
    if filename is None or compiler_id is None or user_id is None or task_id is None or source is None:
        app.logger.error('Not enough info about compiling program')
        abort(400, message='Enter missing info')
    data = {
        'filename' : filename,
        'compiler_id' : compiler_id,
        'user_id' : user_id,
        'task_id' : task_id,
        'source' : source
    }
    print(data)
    print(json.dumps(data))
    with DatabaseConnection() as dbconn:
        dbconn.insert_raw_commit(json.dumps(data))
    return jsonify({"result" : "success"}), 200

@app.route('/auth/register', methods=['POST'])
def post_user():
    login = request.json['login']
    password = request.json['password']
    with DatabaseConnection() as dbconn:
        dbconn.register_user(login, encode(password))
    return jsonify({ 'status': 'success' })

@app.route('/auth/login', methods=['POST'])
def get_user():
    login = request.json['login']
    password = request.json['password']
    hashed_password = encode(password)
    with DatabaseConnection() as dbconn:
        hash_from_db = dbconn.get_hash_by_username(login)
    if hashed_password == hash_from_db:
        token = jwt.encode({ 'password' : password }, SECRET_KEY, algorithm='HS256')
        return jsonify({ 'token' : token.decode('ascii') })

@app.route('/auth/verify', methods=['POST'])
def verify_user():
    print(request)
    print(request.json)
    username = request.json['username']
    token = request.headers.get('Authorization')
    payload = jwt.decode(token.encode('ascii'), SECRET_KEY)
    password_hash = encode(payload['password'])
    with DatabaseConnection() as dbconn:
        hash_from_db = dbconn.get_hash_by_username(username)
    if password_hash == hash_from_db:
        return jsonify({ 'status': 'success' }), 200
    return jsonify({ 'status': 'danger' }), 400

@app.route('/compilers', methods=['GET'])
def get_compilers():
        with DatabaseConnection() as dbconn:
            return dbconn.get_compiler_list()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return ''

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5004
        , debug=True
        )
