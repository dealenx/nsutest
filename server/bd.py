import mysql.connector 
import datetime 
import json

def loadProgram(data, conn):
        cursor = conn.cursor()
        req = "insert into s_tasks(lang, time, file_name, uid, state, source) values( " + data['lang'] + ", sysdate(), '" + data['file_name'] + "',"+ data['uid'] +", 'wait', '"+ data['source'] + "');"
        cursor.execute(req);
        conn.commit()

def loadTestResult():
	print('loadTestResult')

def getProgByID(id, conn):
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