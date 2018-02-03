import mysql.connector
import sys
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

#####################################################################3
##  Вспомогательная херня

    _commit_keys = (\
            'commit_id',\
            'user_id',\
            'task_id',\
            'compiler_id',\
            'filename',\
            'source',\
            'commit_time',\
            'status',\
            'result_code',\
            'output',\
            )


    def validate_status(self, status):
        if status == 'SUBMITTED' or\
        status == 'TESTING' or\
        status == 'TESTED':
                return True
        else:
            return False


    def validate_result_code(self, result_code):
        if result_code == 'OK' or\
        result_code == 'RUNTIME_ERROR' or\
        result_code == 'TIME_LIMIT' or\
        result_code == 'MEMORY_LIMIT' or\
        result_code == 'SYSTEM_TIME_LIMIT' or\
        result_code == 'SECURITY_VIOLATION' or\
        result_code == 'WRONG_ANSWER' or\
        result_code == 'INVALID_INPUT' or\
        result_code == 'COMPILATION_ERROR':
                return True
        else:
            return False


    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


#################################################################3##
## Запрос коммитов из базы данных

    def query_commits_by_commit_id(self, commit_id):
        query=("SELECT * FROM commits WHERE commit_id=%s")
        self._db_cursor.execute(query, (commit_id,))

        dict_result = [dict(zip(self._commit_keys, i)) for i in self._db_cursor.fetchall()]
        json_result = json.dumps(dict_result, default = self.myconverter)
        return json_result


    def query_commits_by_user_id(self, user_id):
        query=("SELECT * FROM commits WHERE user_id=%s")
        self._db_cursor.execute(query, (user_id,))

        dict_result = [dict(zip(self._commit_keys, i)) for i in self._db_cursor.fetchall()]
        json_result = json.dumps(dict_result, default = self.myconverter)
        return json_result


    def query_commits_by_task_id(self, task_id):
        query=("SELECT * FROM commits WHERE task_id=%s")
        self._db_cursor.execute(query, (task_id,))

        dict_result = [dict(zip(self._commit_keys, i)) for i in self._db_cursor.fetchall()]
        json_result = json.dumps(dict_result, default = self.myconverter)
        return json_result


    def query_commits_by_user_id_and_task_id(self, user_id, task_id):
        query=("SELECT * FROM commits WHERE user_id=%s AND task_id=%s")
        self._db_cursor.execute(query, (user_id, task_id))

        dict_result = [dict(zip(self._commit_keys, i)) for i in self._db_cursor.fetchall()]
        json_result = json.dumps(dict_result, default = self.myconverter)
        return json_result


    def query_commits_by_status(self, status):
        if not self.validate_status(status):
            raise Exception('Invalid status specified!')

        query=("SELECT * FROM commits WHERE status=%s")
        self._db_cursor.execute(query, (status,))

        dict_result = [dict(zip(self._commit_keys, i)) for i in self._db_cursor.fetchall()]
        json_result = json.dumps(dict_result, default = self.myconverter)
        return json_result

#################################################################3##
## Вставка нового коммита

#asserts JSON in next format:
#{
#    "user_id": Number,
#    "task_id": Number,
#    "compiler_id": Number,
#    "filename": String,
#    "source": String
#}

    def insert_new_commit(self, json_data):
        data = json.loads(json_data)

        if not 'user_id' in data or\
	    not 'task_id' in data or\
	    not 'compiler_id' in data or\
	    not 'filename' in data or\
	    not 'source' in data:
                raise Exception('Invalid JSON recieved!')

        query=("INSERT INTO commits (user_id, task_id, compiler_id, filename, source) VALUES (%(user_id)s, %(task_id)s, %(compiler_id)s, %(filename)s, %(source)s)")

        self._db_cursor.execute(query, data)
        self._db_connection.commit()


#######################################################
# Редактирование коммитов

    def update_status(self, commit_id, status):

        if self.query_commits_by_commit_id(commit_id) is []:
            raise Exception('Commit with specified ID doesnt exists!')

        if not self.validate_status(status):
            raise Exception('Invalid status specified!')

        query=("UPDATE commits SET status=%s WHERE commit_id=%s")
        self._db_cursor.execute(query, (status, commit_id))
        self._db_connection.commit()


#asserts JSON in next format:
#{
#    "commit_id": Number,
#    "result_code": String,
#    "output": String
#}
    def update_result(self, json_data):
        data = json.loads(json_data)

        if not 'commit_id' in data or\
	    not 'result_code' in data or\
	    not 'output' in data:
                raise Exception('Invalid JSON recieved!')

        if self.query_commits_by_commit_id(data['commit_id']) is []:
            raise Exception('Commit with specified ID doesnt exists!')

        if not self.validate_result_code:
            raise Exception('Invalid result code specified!')

        query="UPDATE commits SET status='TESTED', result_code=%(result_code)s, output=%(output)s WHERE commit_id=%(commit_id)s"

        self._db_cursor.execute(query, data)
        self._db_connection.commit()
        print(data)


#######################################################
# ФУНКЦИИ ДЛЯ РАБОТЫ С API КЛИЕНТА

    def get_not_tested_commit(self):
        json_commits = self.query_commits_by_status("SUBMITTED")
        dict_commits = json.loads(json_commits)

        if not dict_commits:
            return "[]"
        else:
            self.update_status(dict_commits[0]["commit_id"], "TESTING")
            return json.dumps(dict_commits[0])


#######################################################:3
# functions for user control

    def register_user(self, username, hashed_password):
        query=('INSERT INTO users (username, hash) VALUES (%s, %s)')
        self._db_cursor.execute(query, (username, hashed_password))
        self._db_connection.commit()


    def get_hash_by_username(self, username):
        query=('SELECT hash FROM users WHERE username=%s')
        self._db_cursor.execute(query, (username,))
        hashed_password = self._db_cursor.fetchone()[0]
        return hashed_password


    def get_uid_by_username(self, username):
        query=('SELECT user_id FROM users WHERE username=%s')
        self._db_cursor.execute(query, (username,))
        uid = self._db_cursor.fetchone()[0]
        return uid


########################################################
# functions for getting compiler/user/task lists

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
        print(dbconn.get_compiler_list())

