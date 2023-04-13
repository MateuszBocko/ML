#!/usr/bin/python
import psycopg2
import os
from DB.config import config
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)

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
            return cur.fetchone()
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

key = Fernet.generate_key()
if __name__ == '__main__':
    # create class instance
    db_ops = DatabaseOperations()

    data = [(encrypt('login haslo2'.encode(), key))]
    for i in data:
        print(i)
        db_ops.execute_queries(insert_data('USERS', ['CREDENTIALS']), (psycopg2.Binary(i),))

    # commit changes and close conn
    db_ops.commit_changes()

