from flask import Flask, request, abort, jsonify, render_template
import json
import mysql.connector
from mysql.connector import MySQLConnection, Error
import datetime

from db_api import *

app = Flask(__name__, static_folder="../dist", template_folder="../static")

def has_unverified_programs():
 return bdHasUnverifiedProgram(conn);


def get_unverified_programs():
 return bdGetUnverifiedProgram(conn);
 
 
@app.route('/')
def index():
 return render_template("index.html")


@app.route('/load_program', methods=['POST'])
def load_program_from_user():
    print("Inside load_task")
    if not request.json \
    or not 'file_name' in request.json \
    or not 'lang' in request.json \
    or not 'uid' in request.json \
    or not 'source' in request.json:
        abort(400)

    bdLoadProgram(request.json,conn)
    return jsonify({"Result" : "Success"}), 201

@app.route('/programs/check', methods=['GET'])
def get_programs_check():
	return jsonify({'check': bdHasUnverifiedProgram(conn)})

@app.route('/programs/unverified', methods=['GET'])
def get_programs_unverified():
	return get_unverified_programs()

@app.route('/lang', methods=['GET'])
def get_lang():
	return bdGetLang(conn)

@app.route('/check_program', methods=['GET'])
def check_tasks():
 if has_unverified_tasks():
  task_to_verify = het_unverified_task()
  return jsonify(task_to_verify)
 else:
  abort(404)


@app.route('/programs/load', methods=['POST'])
def load_results():
    if not request.json \
    or not 'id' in request.json \
	or not 'client_out' in request.json:
        abort(400)

    test_results = {
        'test_id': request.json['id'],
        'client_out': request.json['client_out'],
    }

    bdLoadResultsProgram(test_results, conn)


if __name__ == '__main__':
	with DatabaseConnection() as dbconn:
		#dbconn.insert_raw_commit('{"user_id": "2", "task_id": "1", "compiler_id": "2", "filename": "test1.c", "source": "#include <stdio.h>dsadsa"}')
		#dbconn.register_user('ayya', 12345)
		dbconn.get_uid_by_username('ayya')
		#app.run(host='0.0.0.0', port=7777)
