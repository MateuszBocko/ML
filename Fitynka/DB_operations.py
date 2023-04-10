import sqlite3
from sqlite3 import Error
import os
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)

class DatabaseOperations:
    def __init__(self):
        self.conn = None

    def connect_to_db(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        """
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def run_query(self, query, bytes):
        c = self.conn.cursor()
        c.execute(query, bytes)

    def commit_query(self):
        self.conn.commit()

    def close_conn(self):
        self.conn.close()

def main(path_to_db, query, bytes):
    db_ops = DatabaseOperations()
    db_ops.connect_to_db(path_to_db)

    db_ops.run_query(query, bytes)
    db_ops.commit_query()
    db_ops.close_conn()

PATH_TO_DB = r"C:\Users\mateu\PycharmProjects\Private_projects\Fitynka\DB\pythonsqlite.db"
creds = 'mateo gowno'

key = Fernet.generate_key()
token = encrypt(creds.encode(), key)

query = """
        INSERT INTO users
        (CREDENTIALS)
        VALUES (?) """
bytes = (sqlite3.Binary(token), )

if __name__ == '__main__':
    main(PATH_TO_DB, query, bytes)