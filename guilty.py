import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from PyQt5 import QtWidgets, uic

import pyqtgraph as pg
import sys


font_path = "C:\\Windows\\Fonts\\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

form_class = uic.loadUiType("guilist.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.name=['광주북부경찰서','광주광산경찰서','광주서부경찰서','광주남부경찰서','광주동부경찰서']
        self.name2=['경찰서','발생건수', '검거건수', '검거인원', '구속', '불구속', '기타']
        self.gwangsan.clicked.connect(self.num5)
        self.east.clicked.connect(self.num1)
        self.west.clicked.connect(self.num2)
        self.south.clicked.connect(self.num3)
        self.north.clicked.connect(self.num4)
        self.allspace.clicked.connect(self.path3)
        self.allspace2.clicked.connect(self.path2)
        self.allspace3.clicked.connect(self.path1)
        self.cl.clicked.connect(self.path4)
        self.nex.clicked.connect(self.fin)
        self.lineEdit1.returnPressed.connect(self.fin2)
        self.back1.clicked.connect(self.back)
        self.guilb.clicked.connect(self.back2)
        self.back_2.clicked.connect(self.back)

        self.con()

        # 그래프 관련 버튼 클릭시 해당 메서드로 연결
        self.generation_btn.clicked.connect(self.generation_graph)
        self.arrest_unarrest_btn.clicked.connect(self.arrest_unarrest_graph)
        # 그래프에 들어갈 내용 전체 리스트
        self.total_graph_list=[]

    # 파이차트 만들기 위해 비율 계산하는 매서드
    def piegraph_ready(self):
        generation_sum=0
        arrest_sum=0
        unarrest_sum=0
        unarrest=[]
        generation_list=[]
        arrest_list=[]
        unarrest_list=[]

        # 발생건수 계 구하기
        for i in range(len(self.a)):
            generation_sum += self.a[i][1]
        # 검거건수 계 구하기
        for j in range(len(self.a)):
            arrest_sum += self.a[j][2]
        # 미검거건수 계 구하기
        unarrest_sum=generation_sum - arrest_sum

        # 미검거건수 리스트 만들기
        for i in range(len(self.a)):
            unarrest.append(self.a[i][1]-self.a[i][2])

        # 발생건수, 전체발생건수 값에서 각 구별 퍼센트 값 구하기
        for i in range(len(self.a)):
            a=(self.a[i][1]/generation_sum) *100
            generation_list.append(a)
        # 검거건수, 발생건수값에서 각 구별 퍼센트 값 구하기
        for i in range(len(self.a)):
            a=(self.a[i][2]/generation_sum) *100
            arrest_list.append(a)
        # 미검거건수, 발생건수값에서 각 구별 퍼센트 값 구하기
        for i in range(len(self.a)):
            a=(unarrest[i]/generation_sum) *100
            unarrest_list.append(a)

        self.total_graph_list=[generation_list,arrest_list,unarrest_list,['동부','서부','남부','북부','광산']
            ,['범죄 발생건수','범죄 검거/미검거건수'],['동부검거건수','서부검거건수','남부검거건수','북부검거건수','광산검거건수']
            ,['동부미검거건수','서부미검거건수','남부미검거건수','북부미검거건수','광산미검거건수']]

        print(self.total_graph_list)

    # 관할별 발생건수 그래프
    def generation_graph(self):
        self.piegraph_ready()
        ratio = [self.total_graph_list[0][0], self.total_graph_list[0][1], self.total_graph_list[0][2],
                 self.total_graph_list[0][3], self.total_graph_list[0][4]]
        labels = [self.total_graph_list[3][0], self.total_graph_list[3][1], self.total_graph_list[3][2],
                  self.total_graph_list[3][3], self.total_graph_list[3][4]]
        explode = [0.03, 0.03, 0.03, 0.03, 0.03]

        plt.pie(ratio, labels=labels, autopct='%.1f%%', explode=explode)
        plt.title(f'관할별 {self.total_graph_list[4][0]}')
        plt.show()
    # 관할별 검거건수, 미검거건수 그래프
    def arrest_unarrest_graph(self):
        self.piegraph_ready()
        ratio = [self.total_graph_list[1][0], self.total_graph_list[1][1], self.total_graph_list[1][2],
                self.total_graph_list[1][3], self.total_graph_list[1][4], self.total_graph_list[2][0],
                 self.total_graph_list[2][1],self.total_graph_list[2][2],self.total_graph_list[2][3],
                 self.total_graph_list[2][4]]
        labels = [self.total_graph_list[5][0], self.total_graph_list[5][1], self.total_graph_list[5][2],
                self.total_graph_list[5][3], self.total_graph_list[5][4],self.total_graph_list[6][0],
                self.total_graph_list[6][1], self.total_graph_list[6][2],self.total_graph_list[6][3],
                self.total_graph_list[6][4]]

        explode = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

        plt.pie(ratio, labels=labels, autopct='%.1f%%', explode=explode)
        plt.title(f'관할별 {self.total_graph_list[4][1]}')
        plt.show()

    def con(self):
        con = pymysql.connect(host='localhost', user='root', password='1234',
                              db='crime', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()
        # sql = "Select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`"#case1
        sql = "Select * from `crime`.`category`"  # case2
        cur.execute(sql)
        self.a = cur.fetchall()
        print(self.a)
    def fin(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tableWidget.setRowCount(0)
    def back(self):
        self.stackedWidget.setCurrentIndex(0)
    def back2(self):
        self.stackedWidget.setCurrentIndex(3)
    def path1(self):
        self.all(1)
    def path2(self):
        self.all(2)
    def path3(self):
        self.all(3)
    def path4(self):
        self.all(4)
    def fin2(self):
        word=self.lineEdit1.text()
        if word in self.name:
            self.fill2(word)
        else:
            self.fill()
    def fill(self):
        count = 0
        count3 = 1
        lis = []
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(self.name2)
        self.tableWidget.setColumnCount(7)
        for i in self.a:
            lis.append(i)
            self.tableWidget.setRowCount(count3)
            count3+=1
        for j in lis:
            count2 = 0
            for k in j:
                self.tableWidget.setItem(count, count2, QTableWidgetItem(str(k)))
                print(count, count2, k)
                count2 += 1
            count += 1

    def fill2(self,word):
        self.tableWidget.setRowCount(0)
        for i in self.a:
            if i[0] == word:
                for j in range(9):
                    self.tableWidget.setRowCount(1)
                    self.tableWidget.setItem(0, j, QTableWidgetItem(str(i[j])))

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
        for i in self.a[n]:
            gra.append(i)
        plt.bar(['발생건수', '검거건수', '검거인원', '구속', '불구속', '기타'], [gra[1], gra[2], gra[3], gra[4], gra[5], gra[6]])
        plt.show()
    def all(self,num):
        n=[0,1,2,3,4]
        gra2=[]
        xlab = ['광주북구','광주광산구','광주서구','광주남구','광주동구']
        xval = list(range(1, len(xlab) + 1))

        ticks = []
        for i, item in enumerate(xlab):
            ticks.append((xval[i], item))
        ticks = [ticks]
        for h in n:
            i=self.a[h]
            gra2.append(i[1])
        plus = (gra2[0] + gra2[1] + gra2[2] + gra2[3] + gra2[4]) / 5
        bargraph=pg.BarGraphItem(x=xval,height=[gra2[3],gra2[4],gra2[1],gra2[2],gra2[0]],width=0.5)
        ax = self.widget.getAxis('bottom')
        ax.setTicks(ticks)
        if num==4:
            self.widget.clear()
        if num==1:
            self.widget.addItem(bargraph)
        if num==2:
            self.widget.plot([1, 2, 3, 4, 5], [gra2[3],gra2[4],gra2[1],gra2[2],gra2[0]], pen='b',symbol='o')
        if num==3:
            self.widget.plot([0,1,2,3,4,5,6],[plus,plus,plus,plus,plus,plus,plus], pen='r',fillLevel=0,fillBrush=(255,255,255,70))
        # plt.show()

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

