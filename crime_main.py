import pymysql
import sqlite3
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

c = conn.cursor()

c.execute('select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`')
a = c.fetchall()
print(a)