import mysql.connector
from mysql.connector import MySQLConnection, Error
from config_parser import read_db_config
import datetime
import json

class DatabaseConnection(object):

    def __enter__(self):
        try:
            db_config = read_db_config()
            self._db_connection = MySQLConnection(**db_config)
            self._db_cursor = self._db_connection.cursor()
            return self
        except Error:
            raise Exception('Can\'t establish connection with database!')


    def __exit__(self, type, value, traceback):
        self._db_cursor.close()
        self._db_connection.close()


    def jsonify(self, table_row):
        if table_row is None:
            return json.dumps(table_row)

        fields = map(lambda x:x[0], self._db_cursor.description)
        result = dict(zip(fields, table_row))

        # we need convert datetime struct to string
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        j_result = json.dumps(result, default = myconverter)
        return j_result


    def query_commit_by_id(self, commit_id):
        self._db_cursor.execute("SELECT * FROM Submits WHERE id = " + str(commit_id))
        row = self._db_cursor.fetchone()
        return self.jsonify(row)


    def query_commits(self, params = None):
        if params is None:
            self._db_cursor.execute("SELECT * FROM Submits")
        else:
            self._db_cursor.execute("SELECT * FROM Submits WHERE " + params)

        # gets commits IDs
        commit_ids = [item[0] for item in self._db_cursor.fetchall()]
        # convert IDs to dictionaries
        dict_list = [json.loads(self.query_commit_by_id(i)) for i in commit_ids]

        print(json.dumps(dict_list))



    '''
    asserts JSON in next format:
    {
        "user_id": Number,
        "task_id": Number,
        "compiler_id": Number,
        "filename": String,
        "source": String
    }
    '''
    def insert_raw_commit(self, j_data):
        data = json.loads(j_data)

        self._db_cursor.execute("INSERT INTO commits ("\
                + ", ".join(data.keys())\
                + ") VALUES (\"" + "\", \"".join(data.values())\
                + "\");")
        self._db_connection.commit()

        self._db_cursor.execute("INSERT INTO commits")


    def register_user(self, username, hashed_password):
        self._db_cursor.execute('INSERT INTO users (username, hash) VALUES (\"{0}\", \"{1}\");'.format(username, hashed_password))
        self._db_connection.commit()


    def get_hash_by_username(self, username):
        self._db_cursor.execute("SELECT hash FROM users WHERE username = \"{0}\"".format(username))
        hashed_password = self._db_cursor.fetchone()[0]
        return hashed_password


    def get_uid_by_username(self, username):
        self._db_cursor.execute("SELECT user_id FROM users WHERE username = \"{0}\"".format(username))
        uid = self._db_cursor.fetchone()[0]
        return uid


if __name__ == '__main__':
    with DatabaseConnection() as dbconn:
        #dbconn.insert_raw_commit('{"user_id": "2", "task_id": "1", "compiler_id": "2", "filename": "test1.c", "source": "#include <stdio.h>dsadsa"}')
        #dbconn.register_user('ayya', 12345)
        dbconn.get_uid_by_username('ayya')



