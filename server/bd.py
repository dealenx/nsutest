import mysql.connector 
import datetime 
import json


def loadProgram(data):
	print('loadProgram')

	cursor = conn.cursor()
	
	jsonToPython = json.loads(data)
	
	dataArray = {
		'file_name': jsonToPython["file_name"],
		'uid': jsonToPython["uid"],
		'lang': jsonToPython["lang"],
		'source': jsonToPython["source"],
		'json_data': jsonToPython
	}

	cursor.execute("insert into s_tasks(lang, time, file_name, uid, state, source) values(" + dataArray["lang"] + ", sysdate(), '" + dataArray["file_name"] + "', " + dataArray["uid"] + ", 'wait', '" + dataArray["source"] + "');")
	conn.commit()
	print(data)
	
	
def loadTestResult():
	print('loadTestResult') 
	
def getProgByID(id):
	print('getProgByID') 
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
	"uid": "' + str(dataArray["uid"]) +  '" } ' 
	return(data)
	
if __name__ == "__main__":
	conn = mysql.connector.connect(host='localhost', 
	database='pythonweb', 
	user='root', 
	password='1040113') 
	
	'''
	jsonData = '{ "file_name": "main.cpp", "uid": "1", "lang": "1", "source": "void main()"}'
	loadProgram(jsonData)
	'''
	print(getProgByID(14))
	conn.close()