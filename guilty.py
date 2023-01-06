import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ElisaBluebell_test import CrimeTablePage
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
        self.gwangsan.clicked.connect(lambda: self.num1(4))
        self.east.clicked.connect(lambda: self.num1(0))
        self.west.clicked.connect(lambda: self.num1(1))
        self.south.clicked.connect(lambda: self.num1(2))
        self.north.clicked.connect(lambda: self.num1(3))
        self.allspace.clicked.connect(lambda: self.path1(3))
        self.allspace2.clicked.connect(lambda: self.path1(2))
        self.allspace3.clicked.connect(lambda: self.path1(1))
        self.cl.clicked.connect(lambda: self.path1(4))
        self.nex.clicked.connect(self.fin)
        self.tableWidget.cellChanged.connect(self.rev)
        self.lineEdit1.returnPressed.connect(self.fin2)
        self.lineEdit2.returnPressed.connect(self.ins)
        self.back1.clicked.connect(lambda: self.back(0))
        self.guilb.clicked.connect(lambda: self.back(3))
        self.guilb2.clicked.connect(lambda: self.back(2))
        self.guilb3.clicked.connect(self.another_path)
        self.back_2.clicked.connect(lambda: self.back(0))
        self.delb.clicked.connect(self.del1)
        self.statusbar = self.statusBar()
        self.gra2=[]
        self.con1()
        self.img()

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

        plt.pie(ratio, labels=labels, autopct='%.1f%%', explode=explode, startangle=260,
                )
        plt.title(f'관할별 {self.total_graph_list[4][1]}')
        plt.show()

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

    def back(self,n):
        self.stackedWidget.setCurrentIndex(n)

    def path1(self,n):
        self.all(n)

    def fin2(self):
        word=self.lineEdit1.text()
        if word in self.name:
            self.fill2(word)
        else:
            self.fill()

    def fill(self):
        self.con1()
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
                # print(count, count2, k)
                count2 += 1
            count += 1

    def fill2(self,word):
        self.con1()
        self.tableWidget.setRowCount(0)
        for i in self.a:
            if i[0] == word:
                for j in range(7):
                    self.tableWidget.setRowCount(1)
                    self.tableWidget.setItem(0, j, QTableWidgetItem(str(i[j])))

    def rev(self):
        self.con1()
        count1=0
        row=self.tableWidget.currentRow()
        col=self.tableWidget.currentColumn()

        sql = "Select * from `crime`.`category`"
        self.cur.execute(sql)
        self.a = self.cur.fetchall()
        for i in self.a:
            if row==count1:
                item=self.tableWidget.currentItem().text()
                cols=(i[0])
                # self.cur.execute(f"UPDATE `crime`.`category` SET 기타= 369 where 경찰서='광주동부경찰서'")
                self.cur.execute(f"UPDATE `crime`.`category` SET {self.name2[col]}={item} where 경찰서='{cols}'")
                self.con.commit()
                # print(i[6],self.name2[col])
                # break
            count1+=1

    def ins(self):
        self.con1()
        word = self.lineEdit2.text()
        words = word.split(',')
        self.cur.execute(f"insert into `crime`.`category` values('{words[0]}',{words[1]},{words[2]},{words[3]},{words[4]},{words[5]},{words[6]})")
        self.con.commit()
        self.lineEdit2.clear()

    def del1(self):
        row=self.tableWidget.currentRow()
        col=self.tableWidget.currentColumn()
        item=self.tableWidget.item(row, col).text()
        # print(item)
        self.cur.execute(f"DELETE FROM `crime`.`category` WHERE 경찰서='{item}'")
        self.con.commit()

    def num1(self,n):
        self.g(n)

    def g(self,num):
        n = num
        gra = []
        for i in self.a[n]:
            gra.append(i)
        plt.bar(['발생건수', '검거건수', '검거인원', '구속', '불구속', '기타'], [gra[1], gra[2], gra[3], gra[4], gra[5], gra[6]])
        plt.show()

    def mouseMoveEvent(self, e):
        txt = "Mouse 위치 ; x={0},y={1}, global={2},{3}".format(e.x(), e.y(), e.globalX(), e.globalY())
        # self.statusbar.showMessage(txt)
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
        self.con1()
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
            self.gra2 = []
            self.widget.clear()
        if num==1:
            self.widget.addItem(bargraph)
        if num==2:
            self.widget.plot([1, 2, 3, 4, 5], [gra2[3],gra2[4],gra2[1],gra2[2],gra2[0]], pen='b',symbol='o')
        if num==3:
            self.widget.plot([0,1,2,3,4,5,6],[plus,plus,plus,plus,plus,plus,plus], pen='r',fillLevel=0,fillBrush=(255,255,255,70))
    def another_path(self):
        widget.setCurrentIndex(1)
    def img(self):
        urlString = 'https://images.chosun.com/resizer/NP8DFExtYcd9QKP1fJrf9YBDC2c=/1200x630/smart/cloudfront-ap-northeast-1.images.arcpublishing.com/chosun/UUXIQJGYI5BN7E6DWOERW5YNAY.JPG'
        imageFromWeb = urllib.request.urlopen(urlString).read()
        qPixmapVar = QPixmap()
        qPixmapVar.loadFromData(imageFromWeb)
        self.backimg.setPixmap(QPixmap(qPixmapVar).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.backimg2.setPixmap(QPixmap(qPixmapVar).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.backimg3.setPixmap(QPixmap(qPixmapVar).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.backimg4.setPixmap(QPixmap(qPixmapVar).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.label_2.setStyleSheet("background-color: white")
        self.label_3.setStyleSheet("background-color: white")

if __name__ == "__main__" :

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    Window1 = WindowClass()
    Window2 = CrimeTablePage()

    widget.addWidget(Window1)
    widget.addWidget(Window2)

    widget.setFixedHeight(768)
    widget.setFixedWidth(1024)

    widget.show()
    app.exec_()