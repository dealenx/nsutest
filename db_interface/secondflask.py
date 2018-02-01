#from flask import Flask
#from flask_restful import Api, Resource

import mysql.connector
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

#application = Flask(__name__)
#api = Api(application)

def connect():
    db_config = read_db_config()

    try:
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to database')
        else:
            print('Connection failed')

    except Error as e:
        print(e)

    finally:
        conn.close()
        print('Connection closed')


def query_with_fetchone():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Submits")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


#class RawSubmitAPI(Resource):
#    def get(self):
#if ... ...
#else
#        return {'result':'no raw tasks'}

#api.add_resource(RawSubmitAPI, '/raw_submits')

if __name__ == '__main__':
    #application.run()
    query_with_fetchone()

