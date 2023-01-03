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
        self.cctv_situation()

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
        # 광산
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='crime')
        c = conn.cursor()
        c.execute("SELECT 소재지지번주소,카메라대수 FROM crime.광주광역시_cctv_20220429 where 소재지지번주소 like '%광산구%'")
        temp = c.fetchall()
        self.gwangsancctv=0
        for i in range(len(temp)):
            self.gwangsancctv += temp[i][1]

        # 북구
        c.execute("SELECT 소재지지번주소,카메라대수 FROM crime.광주광역시_cctv_20220429 where 소재지지번주소 like '%북구%'")
        temp = c.fetchall()
        self.bukgucctv=0
        for i in range(len(temp)):
            self.bukgucctv += temp[i][1]

        # 남구
        c.execute("SELECT 소재지지번주소,카메라대수 FROM crime.광주광역시_cctv_20220429 where 소재지지번주소 like '%남구%'")
        temp = c.fetchall()
        self.namgucctv=0
        for i in range(len(temp)):
            self.namgucctv += temp[i][1]

        # 서구
        c.execute("SELECT 소재지지번주소,카메라대수 FROM crime.광주광역시_cctv_20220429 where 소재지지번주소 like '%서구%'")
        temp = c.fetchall()
        self.seogucctv=0
        for i in range(len(temp)):
            self.seogucctv += temp[i][1]

        # 동구
        c.execute("SELECT 소재지지번주소,카메라대수 FROM crime.광주광역시_cctv_20220429 where 소재지지번주소 like '%동구%'")
        temp = c.fetchall()
        self.dongucctv = 0
        for i in range(len(temp)):
            self.dongucctv += temp[i][1]
        self.cctv_list=[['광주광역시 광산구',self.gwangsancctv],['광주광역시 북구',self.bukgucctv],['광주광역시 남구',self.namgucctv],['광주광역시 서구',self.seogucctv],['광주광역시 동구',self.dongucctv]]

if __name__ == "__main__" :
    app = QApplication(sys.argv)    #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()        #WindowClass의 인스턴스 생성
    myWindow.show()                 #프로그램 화면을 보여주는 코드
    app.exec_()                     #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드