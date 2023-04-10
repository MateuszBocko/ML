import sqlite3
from sqlite3 import Error
import os

query1 = """INSERT INTO CREDS
            (creds)
            VALUES
            ('TEST')
            """

query = """SELECT * FROM users"""
conn = sqlite3.connect(r"C:\Users\mateu\PycharmProjects\Private_projects\Fitynka\DB\pythonsqlite.db")
c = conn.cursor()
c.execute(query)
#conn.commit()
print(c.fetchall())