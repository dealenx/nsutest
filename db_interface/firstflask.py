from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json

application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello World!'


def load_raw_task_to_database():
    pass


@app.route('/load_task', methods=['POST'])
def load_task_from_user():
    if not request.json \
            or not 'file_name' in request.json \
            or not 'task_id' in request.json \
            or not 'lang' in request.json \
            or not 'uid' in request.json \
            or not 'source' in request.json:
        abort(400)


    new_task = {
        'file_name': request.json['file_name'],
        'uid': request.json['uid'],
        'task_id': request.json['task_id'],
        'lang': request.json['lang'],
        'source': request.json['source'],
    }

    load_raw_task_to_database(new_task)

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
    application.run()

