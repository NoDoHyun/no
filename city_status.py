import sys
import matplotlib.pyplot as plt
import pymysql
from PyQt5.QtWidgets import *

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

c = conn.cursor()

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


class CityStatus(QWidget):

    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.set_label()
        self.set_button()
        self.set_line()
        self.setGeometry(0, 0, 800, 600)
        self.show()

    def set_label(self):
        pass

    def set_button(self):
        self.back_btn = QPushButton('돌아가기', self)
        self.back_btn.setGeometry(700, 560, 80, 20)

    def set_line(self):
        pass

    def calc(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CityStatus()
    sys.exit(app.exec())
