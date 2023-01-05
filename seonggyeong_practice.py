# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# import pymysql
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# #UI파일 연결
# #단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
# form_class = uic.loadUiType("analyze.ui")[0]
#
# #화면을 띄우는데 사용되는 Class 선언
# class WindowClass(QMainWindow, form_class) :
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.cctv_list = []
#         self.crime_list = []
#         self.people_list = []
#         self.temp2=[]
#         self.total_list = []
#         self.people_show()
#
#         self.graph1_btn.clicked.connect(self.grpah1)
#
#     def grpah1(self):
#         print(self.total_list)
#         a=self.total_list[0][2]
#         b=self.total_list[1][2]
#         c=self.total_list[2][2]
#         d=self.total_list[3][2]
#         e=self.total_list[4][2]
#
#         # plt.plot(['bukgu','gwansangu','seogu','namgu','dongu'],[a,b,c,d,e])
#         # plt.show()
#         # x = np.arange(5)
#         # gu = ['bukgu','gwansangu','seogu','namgu','dongu']
#         # values = [a,b,c,d,e]
#         #
#         # plt.bar(x, values)
#         # plt.xticks(x, gu)
#
#     # 구별 인구수현황 mysql에서 가져오는 함수
#     def people_situation(self):
#         conn = pymysql.connect(host='localhost',
#                                port=3306,
#                                user='root',
#                                passwd='1234',
#                                db='crime')
#         c = conn.cursor()
#         c.execute("SELECT 구분, `인구(명)`, `면적(제곱킬로미터)` FROM crime.자치구별인구현황 order by `자치구별인구현황`.`인구(명)` desc;")
#         temp = c.fetchall()
#         for i in temp:
#             self.people_list.append(list(i))
#
#     # 전체현황 테이블위젯에 보여주는 함수
#     def people_show(self):
#         self.sum()
#         self.tableWidget.setRowCount(len(self.total_list))
#         header_list=['구분','인구','면적','cctv','범죄수']
#         self.tableWidget.setColumnCount(len(header_list))
#         for i in range(len(header_list)):
#             self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header_list[i]))
#             i += 1
#         for i in range(len(self.total_list)):
#             self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.total_list[i][0])))
#         for i in range(len(self.total_list)):
#             self.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.total_list[i][1])))
#         for i in range(len(self.total_list)):
#             self.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.total_list[i][2])))
#         for i in range(len(self.total_list)):
#             self.tableWidget.setItem(i, 3, QTableWidgetItem(str(self.total_list[i][3])))
#         for i in range(len(self.total_list)):
#             self.tableWidget.setItem(i, 4, QTableWidgetItem(str(self.total_list[i][4])))
#
#     # 구별 cctv현황 mysql에서 가져오는 함수
#     def cctv_situation(self):
#         conn = pymysql.connect(host='localhost',
#                                port=3306,
#                                user='root',
#                                passwd='1234',
#                                db='crime')
#         c = conn.cursor()
#         c.execute("select 소재지지번주소 as 구분, sum(카메라대수) as 카메라대수 from `crime`.`광주광역시_cctv_20220429` group by 구분 order by 카메라대수 desc;")
#         temp = c.fetchall()
#         for i in temp:
#             self.cctv_list.append(list(i))
#
#     # 구별 범죄수현황 mysql에서 가져오는 함수
#     def crime_situation(self):
#         conn = pymysql.connect(host='localhost',
#                                port=3306,
#                                user='root',
#                                passwd='1234',
#                                db='crime')
#         c = conn.cursor()
#         c.execute("select 관서명 as 구분, sum(`살인`+`강도`+`강간-강제추행`+`절도`+`폭력`) as 범죄수 from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` group by 관서명 order by 범죄수 desc;")
#         temp = c.fetchall()
#         for i in temp:
#             self.crime_list.append(list(i))
#
#     # 구별 범죄수, 인구수, cctv수 하나의 리스트로 만드는 함수
#     def sum(self):
#         self.cctv_situation()
#         self.crime_situation()
#         self.people_situation()
#
#         for i in range(len(self.people_list)):
#             temp = []
#             for j in range(len(self.cctv_list)):
#                 if self.people_list[i][0] == self.cctv_list[j][0]:
#                     a=self.people_list[i][0]
#                     b=self.people_list[i][1]
#                     c=self.people_list[i][2]
#                     d=self.cctv_list[i][1]
#                     temp.append(a)
#                     temp.append(b)
#                     temp.append(c)
#                     temp.append(d)
#             self.temp2.append(temp)
#
#         for i in range(len(self.temp2)):
#             temp1 = []
#             for j in range(len(self.crime_list)):
#                 if self.temp2[i][0] == self.crime_list[j][0]:
#                     e=self.temp2[i][0]
#                     f=self.temp2[i][1]
#                     g=self.temp2[i][2]
#                     h=self.temp2[i][3]
#                     k=self.crime_list[i][1]
#                     temp1.append(e)
#                     temp1.append(f)
#                     temp1.append(g)
#                     temp1.append(h)
#                     temp1.append(k)
#             self.total_list.append(temp1)
#
# if __name__ == "__main__" :
#     app = QApplication(sys.argv)    #QApplication : 프로그램을 실행시켜주는 클래스
#     myWindow = WindowClass()        #WindowClass의 인스턴스 생성
#     myWindow.show()                 #프로그램 화면을 보여주는 코드
#     app.exec_()                     #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드

import matplotlib.pyplot as plt
import numpy as np
# 그래프 한글깨짐 고치는 방법
from matplotlib import font_manager, rc

header_list=['인구(만명)', '범죄발생건수', '범죄건수(만명)', '범죄건수(km²)', '검거건수', '검거율(%)', '카메라대수','카메라 1대당 인구수']
list=[['동구', '남구', '서구','광산구','북구'],[10,21,29,40,43],[1240,1538,2621,2946,3703]
      ,[120,72,90,73,87],[25.3061,25.2131,54.6042,13.2108,30.8583],[1056,1147,2100,2360,2873]
      ,[85.1613,74.5774,80.1221,80.1086,77.5857],[954,1511,1798,2383,2341]
    ,[108.1604,141.7015,162.8053,169.7113,182.8449]]
donggu_average_list=[[sum(list[1])/5],[sum(list[3])/5],[sum(list[6])/5],[sum(list[8])/5]]

# 1. 기본 스타일 설정
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 9)
plt.rcParams['font.size'] = 10
font_path = "C:\\Windows\\Fonts\\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 2. 데이터 준비
x = np.arange(4)
data=(['population(10,000)','number of crimes(10,000)','arrest rate','population(per camera)'])
y1 = np.array([donggu_average_list[0], donggu_average_list[1], donggu_average_list[2], donggu_average_list[3]])
y2 = np.array([list[1][0], list[3][0], list[6][0], list[8][0]])

# 3. 그래프 그리기
fig, ax1 = plt.subplots()

ax1.plot(x, y1, color='green', markersize=7, linewidth=5, alpha=0.7, label='total average')
ax1.set_ylim(0, 200)
ax1.set_xlabel('요소')
ax1.set_ylabel('total average')

ax2 = ax1.twinx()
ax2.bar(x, y2, color='deeppink', label='야옹', alpha=0.7, width=0.7)
ax2.set_ylim(0, 200)
ax2.set_ylabel(r'element_value')

ax1.set_zorder(ax2.get_zorder() + 10)
ax1.patch.set_visible(False)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.title('동구 그래프')
plt.xticks(x, data)

plt.show()
