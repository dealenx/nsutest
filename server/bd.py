import mysql.connector 
import datetime 
import json
from flask import jsonify

def bdLoadProgram(data, conn):
        cursor = conn.cursor()
        req = "insert into s_programs(lang, time, file_name, uid, state, source) values( " + \
		data['lang'] + ", sysdate(), '" + \
		data['file_name'] + \
		"',"+ data['uid'] +", 'wait', '"+ data['source'] + "');"
        cursor.execute(req);
        conn.commit()

def bdLoadResultsProgram(data, conn):
        cursor = conn.cursor()
        req = "update s_programs set client_out = '" + \
		data['client_out'] + "', state = 'ready' where id = " + \
		data['id'] + ";"
        cursor.execute(req);
        conn.commit()
	
def bdLoadResults():
	print('bdLoadResults')
	
def bdHasUnverifiedProgram(conn):
	cursor = conn.cursor()
	cursor.execute("select count(*) count_wait from s_programs where state like 'wait';")
	row = cursor.fetchone()
	while row is not None:
		if (row[0] > 0):
			status = True
		else:
			status = False
		row = cursor.fetchone()
	cursor.close()
    
	return status

def bdGetUnverifiedProgram(conn):
	print('bdLoadResults')
	cursor = conn.cursor()
	cursor.execute("select id from s_programs where state like 'wait' order by time LIMIT 0, 1;")
	row = cursor.fetchone()
	
	while row is not None:
		wait_id = row[0]
		row = cursor.fetchone()
	cursor.close()

	return getProgByID(wait_id, conn)

def bdGetLang(conn):
	print('bdGetLang')
	cursor = conn.cursor()
	cursor.execute("select id, name from s_lang;")
	row = cursor.fetchone()
	req = '['
	while row is not None:
		req = req + '{"id":'+ str(row[0]) + ', "name":' + row[1] + '}'
		row = cursor.fetchone()
	cursor.close()
	req = req + ']' # убрать последнюю запятую
	return req 

def getProgByID(id, conn):
	cursor = conn.cursor()
	cursor.execute("SELECT id, lang, file_name, source, time, client_out, uid  FROM s_programs where id = " + str(id))
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