import mysql.connector 
import datetime 
import json

from bd import loadProgram
conn = mysql.connector.connect(host='localhost', 
	database='pythonweb', 
	user='root', 
	password='1040113') 
	
if __name__ == "__main__":
	conn = mysql.connector.connect(host='localhost', 
	database='pythonweb', 
	user='root', 
	password='1040113') 
	jsonData = '{ "file_name": "main.cpp", "uid": "1", "lang": "1", "source": "void main()"}'
	loadProgram(jsonData, conn)
	conn.close()

