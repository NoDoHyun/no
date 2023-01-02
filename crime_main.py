import pymysql
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

# c = conn.cursor()
# # 발생건수 테스트 출력
# c.execute('select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` where 구분="발  생  건  수"')
# a = c.fetchall()
# print(a)
# c.execute('select * from `crime`.`광주광역시_CCTV_20220429`')
# a = c.fetchall()
# print(a)
# c.execute('select * from `crime`.`광주광역시_자치구별 현황_20210731`')
# a = c.fetchall()
# print(a)

class