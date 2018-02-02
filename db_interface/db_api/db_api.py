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
        self._db_cursor.execute("SELECT * FROM commits WHERE commit_id = " + str(commit_id))
        row = self._db_cursor.fetchone()
        return self.jsonify(row)


    def query_commits(self, params):
        #print("SELECT * FROM commits WHERE " + params)
        self._db_cursor.execute("SELECT * FROM commits WHERE " + params)

        # gets commits IDs
        commit_ids = [item[0] for item in self._db_cursor.fetchall()]
        # convert IDs to dictionaries
        dict_list = [json.loads(self.query_commit_by_id(i)) for i in commit_ids]

        return(json.dumps(dict_list))



    '''
    asserts JSON in next format:
    {
        "user_id": Number,
        "task_id": Number,
        "compiler_id": Number,
        "filename": String,
        "source": String
    }
     |
     |
     |
    \ /
     V
    '''
    def insert_raw_commit(self, j_data):
        data = json.loads(j_data)
        self._db_cursor.execute('INSERT INTO commits (user_id, task_id, compiler_id, filename, source) VALUE ({0}, {1}, {2}, "{3}", "{4}")'\
                .format(data["user_id"], data["task_id"], data["compiler_id"], data["filename"], data["source"]))
        self._db_connection.commit()


    #def modify_commit(self, commit_id, params):



#######################################################
# functions for compiler's API

    def get_not_tested_submit(self):
        lontc = json.loads(self.query_commits(params = 'status = "SUBMITTED"'))
        if not lontc:
            return lontc
        else:
            self._db_cursor.execute('UPDATE commits SET status = "TESTING" WHERE commit_id = {0}'.format(lontc[0]["commit_id"]))
            self._db_connection.commit()
            return json.dumps(lontc[0])



    '''
    asserts JSON in next format:
    {
        "commit_id": Number,
        "result_code": String,
        "output": String
    }
    '''
    def set_test_result(self, j_result):
        result = json.loads(j_result)
        self._db_cursor.execute('UPDATE commits SET status = "TESTED", result_code = "{1}", output = "{2}" WHERE commit_id = {0}'.format(result["commit_id"], result["result_code"], result["output"]))
        self._db_connection.commit()




#######################################################:3
# functions for user control

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


########################################################
# functions for getting compiler/task lists

    def get_compiler_list(self):
        self._db_cursor.execute("SELECT * FROM compilers")

        keys = ["id", "name"]
        result_list = self._db_cursor.fetchall()

        dict_result = [dict(zip(keys, i)) for i in result_list]
        j_result = json.dumps(dict_result)

        return j_result


    def get_task_list(self):
        self._db_cursor.execute("SELECT * FROM tasks")

        keys = ["id", "name", "description"]
        result_list = self._db_cursor.fetchall()

        dict_result = [dict(zip(keys, i)) for i in result_list]
        j_result = json.dumps(dict_result)

        return j_result


if __name__ == '__main__':
    with DatabaseConnection() as dbconn:
        #dbconn.insert_raw_commit('{"user_id": "2", "task_id": 2, "compiler_id": 3, "filename": "testadasdas1.c", "source": "#include <stdio.h>dsadsa"}')
        #dbconn.set_test_result('{"commit_id": 23, "result_code": "COMPILATION_ERROR", "output": "Molodec!!!"}')
        print(dbconn.get_task_list())



