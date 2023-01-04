import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("analyze.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.people_show()
        self.cctv_list = []
        self.cctv_situation()
        self.crime_situation()


    # 구별 인구수현황 mysql에서 가져오는 함수
    def people_situation(self):
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='crime')
        c = conn.cursor()
        c.execute("SELECT `구분`,`인구(명)` FROM `crime`.`자치구별인구현황` order by `자치구별인구현황`.`인구(명)` desc")
        self.people = c.fetchall()

    # 구별 인구수현황 테이블위젯에 보여주는 함수
    def people_show(self):
        self.people_situation()
        self.tableWidget.setRowCount(len(self.people))
        header_list = ['구분', '인구(명)']
        self.tableWidget.setColumnCount(len(header_list))
        for i in range(len(header_list)):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header_list[i]))
            i += 1
        for i in range(len(self.people)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.people[i][0]))
        for i in range(len(self.people)):
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.people[i][1])))

    # 구별 cctv현황 mysql에서 가져오는 함수
    def cctv_situation(self):
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='crime')
        c = conn.cursor()
        c.execute("select sum(카메라대수) as 카메라대수, 소재지지번주소 as 구분 from `crime`.`광주광역시_cctv_20220429` group by 구분 order by 카메라대수 desc;")
        temp = c.fetchall()
        for i in temp:
            self.cctv_list.append(list(i))

    def crime_situation(self):
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='crime')
        c = conn.cursor()
        c.execute("update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='동구' where 관서명='광주동부경찰서';")
        temp = c.fetchall()
        print(temp)


if __name__ == "__main__" :
    app = QApplication(sys.argv)    #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()        #WindowClass의 인스턴스 생성
    myWindow.show()                 #프로그램 화면을 보여주는 코드
    app.exec_()                     #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드

        # "update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='동구' where 관서명='광주동부경찰서'; update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='서구' where 관서명='광주서부경찰서'; update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='북구' where 관서명='광주북부경찰서'; update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='광산구' where 관서명='광주광산경찰서'; update `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` set 관서명='남구' where 관서명='광주남부경찰서'; select 관서명 as 구분, sum(`살인`+`강도`+`강간-강제추행`+`절도`+`폭력`) as 범죄수 from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` group by 관서명 order by 범죄수 desc;")