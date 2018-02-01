from flask import Flask, request, abort, jsonify, render_template
import json
import datetime

from db_api import *

app = Flask(__name__, static_folder="../dist", template_folder="../static")


@app.route('/')
def index():
 return render_template("index.html")


@app.route('/compile', methods=['POST'])
def post_program():
    filename = request.json['file_name']
    compiler_id = request.json['lang']
    user_id = request.json['uid']
    # task_id = request.json['task_id']
    source = request.json['source']
    if filename is None or compiler_id is None or user_id is None or source is None:
        app.logger.error("Not enough info about compiling program")
        abort(400, message="Enter missing info")
    data = {
        'filename' : filename,
        'compiler_id' : compiler_id,
        'user_id' : user_id,
        'task_id' : '1',
        'source' : source
    }
    print(json.dumps(data))
    with DatabaseConnection() as dbconn:
        dbconn.insert_raw_commit(json.dumps(data))
    return jsonify({"result" : "success"}), 200

@app.route('/lang', methods=['GET'])
def get_lang():
        return ''

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
