import pymysql
import sqlite3
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='guest',
                       passwd='1234',
                       db='all.db')

c = conn.cursor()

sqlite3 all.db -batch ".dump" > my_db.sql