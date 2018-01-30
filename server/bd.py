import mysql.connector 
import datetime 

cnx = mysql.connector.connect(host='localhost', 
database='pythonweb', 
user='root', 
password='1040113') 
cursor = cnx.cursor() 

cursor.execute("SELECT * FROM s_tasks where id = 1") 

results = cursor.fetchall() 

print(results) 

cursor.close() 
cnx.close()