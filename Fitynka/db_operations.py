#!/usr/bin/python
import psycopg2
import os
from DB.config import config
from encrypting import hash_new_password


class DatabaseOperations:
    def __init__(self):
        self.conn = None
        self.connect_to_db()

    def connect_to_db(self):
        params = config()
        self.conn = psycopg2.connect(**params)

    def execute_queries(self, query, values = None):

        cur = self.conn.cursor()
        if values == None:
            cur.execute(query)
        else:
            cur.execute(query, values)

        try:
            result = cur.fetchone()
            return result
        except:
            pass

    def commit_changes(self):
        self.conn.commit()
        self.conn.close()

def create_tables():
    # read files in queries folder
    directory = os.fsencode('QUERIES')
    for file in os.listdir(directory):
        filename = os.path.join('QUERIES', os.fsdecode(file))
        fd = open(filename, 'r').read()
        db_ops.execute_queries(fd)

def insert_data(table, columns):
    values = ', '.join(('%s' for element in columns))
    columns = ', '.join(columns)
    query = f"""INSERT INTO {table} ({columns}) VALUES ({values})"""

    return query

def insert_new_user_credentials():
    #TODO JUST A SAMPLE, DO NOT USE FURTHER
    # create class instance
    db_ops = DatabaseOperations()

    data = [
        {
        'login': 'mateo',
        'password': hash_new_password('eloelo')
        }
         ]

    for i in data:
        db_ops.execute_queries(insert_data('USERS', ['LOGIN', 'CREDENTIALS_V1', 'CREDENTIALS_V2']),(i['login'],str(i['password'][0]),str(i['password'][1])))

    # commit changes and close conn
    db_ops.commit_changes()

if __name__ == '__main__':
    # create class instance
    db_ops = DatabaseOperations()

    data = [
        {
        'login': 'mateo',
        'password': hash_new_password('eloelo')
        }
         ]

    for i in data:
        db_ops.execute_queries(insert_data('USERS', ['LOGIN', 'CREDENTIALS_V1', 'CREDENTIALS_V2']),(i['login'],str(i['password'][0]),str(i['password'][1])))

    # commit changes and close conn
    db_ops.commit_changes()

