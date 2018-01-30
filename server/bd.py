import mysql.connector 
import datetime 
import json


def loadProgram(data):
	print('loadProgram')

	
	cursor = conn.cursor()

	cursor.execute("insert into s_tasks(lang, time) values(5, sysdate());")
	conn.commit()
	print(data)
	
def loadTestResult():
	print('loadTestResult') 
	
def getProgByID(id):
	print('getProgByID') 
	cursor = conn.cursor() 
	cursor.execute("SELECT * FROM s_tasks where id = " + str(id)) 
	results = cursor.fetchall() 
	print(results)
	cursor.close() 

if __name__ == "__main__":
	conn = mysql.connector.connect(host='localhost', 
	database='pythonweb', 
	user='root', 
	password='1040113') 
	
	jsonData = '{ "file_name": "main.cpp", "uid": "1", "lang": "1", "source": "void main()"}'
	jsonToPython = json.loads(jsonData)
	
	data = {
		'file_name': jsonToPython["file_name"],
		'uid': int(jsonToPython["uid"]),
		'lang': int(jsonToPython["lang"]),
		'source': jsonToPython["source"],
		'json_data': jsonToPython
	}
	loadProgram(data)
	
	conn.close()