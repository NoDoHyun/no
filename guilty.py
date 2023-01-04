import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
        self.name2=['경찰서','인구(만명)', '범죄발생건수', '범죄발생건수/만명', '범죄발생건수/km²', '검거건수', '검거율(%)', '카메라대수', '인구수/카메라대수']
        self.gwangsan.clicked.connect(self.num5)
        self.east.clicked.connect(self.num1)
        self.west.clicked.connect(self.num2)
        self.south.clicked.connect(self.num3)
        self.north.clicked.connect(self.num4)
        self.allspace.clicked.connect(self.all)
        self.nex.clicked.connect(self.next)
        self.search.clicked.connect(self.fin)
        self.lineEdit1.returnPressed.connect(self.fin2)
        self.back1.clicked.connect(self.back)
        self.con()
    def con(self):
        con = pymysql.connect(host='localhost', user='root', password='1234',
                              db='crime', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()
        # sql = "Select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`"#case1
        # DB에서 경찰서명, 인구수(만명)
        sql = ('select c.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", '
                # 5대 범죄 발생건수를 합산해서 범죄발생건수로 명명해서 가져옴
                'b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수, '
                # 범죄 발생 건수를 인구*만명으로 나눈 값의 소수점을 버려 범죄율 계산
                'round((b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` * 10000) '
                'as "인구 1만명당 범죄 건수", '
                # 면적 대비 범죄율
                '(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / `면적(제곱킬로미터)` '
                'as "범죄 건수/면적(km²)", '
                # 건거검수/범죄발생건수 = 검거율
                'c.검거건수, c.검거건수/(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) * 100 '
                'as "검거율(%)", '
                # 18이 어디서 나왔는지 모르겠음. 18로 나누면 정상값이라 그냥 나눠서 가져옴
                'round(sum(d.카메라대수)/18) as 카메라대수, a.`인구(명)`/(sum(d.카메라대수)/18) '
                'as "카메라 1대당 인구수" '
                # 1번 테이블 as a
                'from `crime`.`광주광역시_자치구별 현황_20210731` as a '
                # 2번 테이블 as b
                'inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b '
                # 3번 테이블 as c
                'inner join `crime`.`category` as c '
                # 4번 테이블 as d
                'inner join `crime`.`광주광역시_cctv_20220429` as d '
                # 접점 생성
                'on mid(d.소재지지번주소, 7, 1) = mid(c.경찰서, 3, 1) '
                'on mid(c.경찰서, 3, 1) = mid(b.관서명, 3, 1) '
                'on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1) '
                # 관서명으로 묶고 범죄발생건수로 정렬해서 광주<광>역시경찰청을 제외한 구경찰서 5개 출력
                'group by 관서명 order by 범죄발생건수 limit 1, 5')
        cur.execute(sql)
        self.a = cur.fetchall()

    def next(self):
        self.stackedWidget.setCurrentIndex(0)

    def fin(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tableWidget.setRowCount(0)

    def back(self):
        self.stackedWidget.setCurrentIndex(3)

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
        self.tableWidget.setColumnCount(9)
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
                    # self.tableWidget.setRowCount(1)
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
    def all(self):
        n=[0,1,2,3,4]
        gra2=[]
        for h in n:
            i=self.a[h]
            gra2.append(i[1])
        plt.bar(['광주북구','광주광산구','광주서구','광주남구','광주동구'],[gra2[3],gra2[4],gra2[1],gra2[2],gra2[0]])
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