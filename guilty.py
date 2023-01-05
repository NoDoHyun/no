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
class WindowClass(QMainWindow, form_class,QtWidgets.QWidget) :
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
        self.tableWidget.cellChanged.connect(self.rev)
        self.lineEdit1.returnPressed.connect(self.fin2)
        self.back1.clicked.connect(self.back)
        self.guilb.clicked.connect(self.back2)
        self.back_2.clicked.connect(self.back)
        self.delb.clicked.connect(self.del1)
        self.statusbar = self.statusBar()
        self.gra2=[]
        self.con1()
    def con1(self):
        self.con = pymysql.connect(host='localhost', user='root', password='1234',
                              db='crime', charset='utf8')  # 한글처리 (charset = 'utf8')
        self.cur = self.con.cursor()
        # sql = "Select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`"#case1
        sql = "Select * from `crime`.`category`"  # case2
        self.cur.execute(sql)
        self.a = self.cur.fetchall()
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
                for j in range(7):
                    self.tableWidget.setRowCount(1)
                    self.tableWidget.setItem(0, j, QTableWidgetItem(str(i[j])))
    def rev(self):
        count1=0
        row=self.tableWidget.currentRow()
        col=self.tableWidget.currentColumn()
        item=self.tableWidget.currentItem().text()
        sql = "Select * from `crime`.`category`"
        self.cur.execute(sql)
        self.a = self.cur.fetchall()
        for i in self.a:
            if row==count1:
                cols=(i[0])
                # self.cur.execute(f"UPDATE `crime`.`category` SET 기타= 369 where 경찰서='광주동부경찰서'")
                self.cur.execute(f"UPDATE `crime`.`category` SET {self.name2[col]}={item} where 경찰서='{cols}'")
                self.con.commit()
                print(i[6],self.name2[col])
                # break
            count1+=1
    def del1(self):
        row=self.tableWidget.currentRow()
        col=self.tableWidget.currentColumn()
        print(row,col)
        self.tableWidget.takeItem(row, col)

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

    def mouseMoveEvent(self, e):
        txt = "Mouse 위치 ; x={0},y={1}, global={2},{3}".format(e.x(), e.y(), e.globalX(), e.globalY())
        self.statusbar.showMessage(txt)
        if e.x()>=449 and e.x()<=484 and e.y()>=228 and e.y()<=621:
            self.label_2.setText(str(self.gra2[3]))
            self.label_3.setText('광주북구')
        elif e.x()>=517 and e.x()<=549 and e.y()>=309 and e.y()<=621:
            self.label_2.setText(str(self.gra2[4]))
            self.label_3.setText('광주광산구')
        elif e.x()>=582 and e.x()<=617 and e.y()>=344 and e.y()<=621:
            self.label_2.setText(str(self.gra2[1]))
            self.label_3.setText('광주서구')
        elif e.x()>=649 and e.x()<=684 and e.y()>=458 and e.y()<=621:
            self.label_2.setText(str(self.gra2[2]))
            self.label_3.setText('광주남구')
        elif e.x()>=716 and e.x()<=751 and e.y()>=490 and e.y()<=621:
            self.label_2.setText(str(self.gra2[0]))
            self.label_3.setText('광주동구')
        else:
            self.label_2.clear()
            self.label_3.clear()
    def all(self,num):
        n=[0,1,2,3,4]
        xlab = ['광주북구','광주광산구','광주서구','광주남구','광주동구']
        xval = list(range(1, len(xlab) + 1))
        self.gra2=[]
        gra2=self.gra2
        ticks = []
        for i, item in enumerate(xlab):
            ticks.append((xval[i], item))
        ticks = [ticks]
        for h in n:
            i=self.a[h]
            self.gra2.append(i[1])
        plus = (gra2[0] + gra2[1] + gra2[2] + gra2[3] + gra2[4]) / 5
        bargraph=pg.BarGraphItem(x=xval,height=[gra2[3],gra2[4],gra2[1],gra2[2],gra2[0]],width=0.1)
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

