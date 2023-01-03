import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

font_path = "C:\\Windows\\Fonts\\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

con = pymysql.connect(host='localhost', user='root', password='1234',
                      db='crime', charset='utf8') # 한글처리 (charset = 'utf8')
cur = con.cursor()
# sql = "Select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`"#case1
sql = "Select * from `crime`.`category`"    #case2
cur.execute(sql)
a= cur.fetchall()

form_class = uic.loadUiType("guilist.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.gwangsan.clicked.connect(self.num5)
        self.east.clicked.connect(self.num1)
        self.west.clicked.connect(self.num2)
        self.south.clicked.connect(self.num3)
        self.north.clicked.connect(self.num4)

    def num1(self):
        self.g(0)
    def num2(self):
        self.g(1)
    def num3(self):
        self.g(2)
    def num4(self):
        self.g(3)
    def num5(self):
        self.g(4)
    def g(self,num):
        n = num
        gra = []
        for i in a[n]:
            gra.append(i)
        plt.bar(['발생건수', '검거건수', '검거인원', '구속', '불구속', '기타'], [gra[1], gra[2], gra[3], gra[4], gra[5], gra[6]])
        plt.show()

if __name__ == "__main__" :

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
# CASE 1
# name=['광주광산경찰서','광주동부경찰서','광주서부경찰서','광주남부경찰서','광주북부경찰서']
# b=[]
# namenum=[]
#
# for i in a:
#     b.append(list(i))
# for k in name:
#     for j in b:
#         if j[0] in k:
#             if j[1] in '발  생  건  수':
#                 c = 0
#                 print(j)
#                 c+=j[2]+j[3]+j[4]+j[5]+j[6]
#                 namenum+=[[k,c]]
#                 break
# print(namenum)



# CASE2

