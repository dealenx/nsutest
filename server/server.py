from flask import Flask, request, abort, jsonify, render_template
import json
import mysql.connector
import datetime


def loadProgram(data):
        cursor = conn.cursor()
        req = "insert into s_tasks(lang, time, file_name, uid, state, source) values( " + data['lang'] + ", sysdate(), '" + data['file_name'] + "',"+ data['uid'] +", 'wait', '"+ data['source'] + "');"
        cursor.execute(req);
        conn.commit()

def loadTestResult():
	print('loadTestResult')

def getProgByID(id):
	cursor = conn.cursor()
	cursor.execute("SELECT id, lang, file_name, source, time, client_out, uid  FROM s_tasks where id = " + str(id))
	row = cursor.fetchone()
	while row is not None:
		dataArray = {
			'id': row[0],
			'lang': row[1],
			'file_name': row[2],
			'source': row[3],
			'time': row[4],
			'client_out': row[5],
			'uid': row[6],
		}
		row = cursor.fetchone()
	cursor.close()
	data = '{ "id": "' + str(dataArray["id"]) +  '", \
	"lang": "' + str(dataArray["lang"]) +  '", \
	"file_name": "' + str(dataArray["file_name"]) +  '", \
	"source": "' + str(dataArray["source"]) +  '", \
	"time": "' + str(dataArray["time"]) +  '", \
	"client_out": "' + str(dataArray["client_out"]) +  '", \
	"task_id": "1", \
	"uid": "' + str(dataArray["uid"]) +  '" } '
	return(data)


app = Flask(__name__, static_folder="../dist", template_folder="../static")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/load_program', methods=['POST'])
def load_task_from_user():
    print("Inside load_task")
    if not request.json \
            or not 'file_name' in request.json \
            or not 'lang' in request.json \
            or not 'uid' in request.json \
            or not 'source' in request.json:
        abort(400)

    loadProgram(request.json)
    return jsonify({"Result" : "Success"}), 201



def has_unverified_tasks():
    pass


def get_unverified_task():
    pass


@app.route('/check_tasks', methods=['GET'])
def check_tasks():
    if has_unverified_tasks():
        task_to_verify = get_unverified_task()
        return jsonify(task_to_verify)
    else:
        abort(404)


@app.route('/load_results', methods=['POST'])
def load_results():
    if not request.json \
            or not 'test_id' in request.json \
            or not 'result' in request.json:
        abort(400)

    test_results = {
        'test_id': request.json['test_id'],
        'result': request.json['result'],
    }

    load_results_to_database(test_results)


if __name__ == '__main__':
    conn = mysql.connector.connect(host='localhost',
    database='pythonweb',
    user='root',
    password='1040113')

    app.run(host='0.0.0.0', port=5001)

    conn.close()
