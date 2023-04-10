import sqlite3
from sqlite3 import Error
import os

class DatabaseCreation:
    def __init__(self):
        self.conn = None

    def create_db(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        """
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def create_table(self, sql_query_file):
        """ create a table from the create_table_sql statement
        :param sql_query: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            with open(sql_query_file, 'r') as sql_file:
                c.execute(sql_file.read())
        except Error as e:
            print(e)

    def close_conn(self):
        self.conn.close()

def main(path_to_db):
    # create class object
    database = DatabaseCreation()

    # create connection to db
    database.create_db(path_to_db)

    # create all tables
    for filename in os.listdir('SQL'):
        sql_query_file = os.path.join('SQL/', filename)
        database.create_table(sql_query_file)

    # close db connection
    database.close_conn()

PATH_TO_DB = r"C:\Users\mateu\PycharmProjects\Private_projects\Fitynka\DB\pythonsqlite.db"
if __name__ == '__main__':
    main(PATH_TO_DB)