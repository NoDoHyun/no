# # =======================================================설정=======================================================
#
# # DB 사용을 위해 세팅
# import pymysql
# # 그래프를 그리기 위해 세팅
# import matplotlib.pyplot as plt
# import numpy as np
# # 한글 폰트 사용을 위해서 세팅
# from matplotlib import font_manager, rc
#
# # =======================================================설정=======================================================
# # ===================================================데이터 핸들링===================================================
#
# # mysql 로그인 및 db 획득
# conn = pymysql.connect(host='localhost',
#                        port=3306,
#                        user='root',
#                        passwd='1234',
#                        db='crime')
#
# # 커서 지정
# c = conn.cursor()
#
# # 발생건수 테스트 출력
# # c.execute('select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` where 구분="발  생  건  수"')
# # a = c.fetchall()
# # print(a)
# # c.execute('select * from `crime`.`광주광역시_CCTV_20220429`')
# # a = c.fetchall()
# # print(a)
# # crime 스키마 내의 광주광역시 자치구별 현황 테이블에서 구분, 세대수, 인구, 공무원, 면적 불러옴
# c.execute('select a.구분, a.세대수, a.`인구(명)`, a.`공무원(명)`, a.`면적(제곱킬로미터)`,'
#           # 공무원 1인당 인구 산출
#           ' round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)",'
#           # 인구밀도 산출
#           ' round(`인구(명)`/`면적(제곱킬로미터)`) as "인구밀도(명/제곱킬로미터)",'
#           # 범죄 발생 건수 산출
#           ' b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수,'
#           # 인구수 대비 범죄율 산출
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` as "범죄 발생건수/인구(명)",'
#           # 인구밀도 대비 범죄율 산출
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / round(`인구(명)`/`면적(제곱킬로미터)`)'
#           ' as "범죄 발생건수/인구밀도(명/km²)",'
#           # 공무원당 담당 인구수 대비 범죄율
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / (`인구(명)`/`공무원(명)`)'
#           ' as "범죄 발생건수/공무원 1인당 시민 수"'
#           # 자치구별 현황을 a로 받아옴
#           'from `crime`.`광주광역시_자치구별 현황_20210731` as a'
#           # 자치구별 5대 범죄 현황을 b로 받아와서 조인
#           ' inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b'
#           # 각 구와 경찰서의 명칭 중 동서남북광이 겹치는 것을 매개로 연결
#           ' on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1)'
#           # 관서명으로 묶어 범죄발생건수(맨 위에 나옴) 제외한 나머지 값 표시제거
#           ' group by 관서명'
#           # 범죄발생건수 오름차순 정렬해서 관할구가 존재하지 않는 시 경찰청을 맨 위로 올림
#           ' order by 범죄발생건수'
#           # 1번째 순서를 제외한 5개 출력으로 시 경찰청 제외한 나머지 출력
#           ' limit 1, 5')
#
# # 테스트용 출력
# # 0 동구 1 남구 2 서구 3 광산구 4 북구
# # 0 구명 1 세대수 2 인구(명) 3 공무원(명) 4 면적(제곱킬로미터) 5 공무원 1인당 인구(명) 6 인구밀도(명/제곱킬로미터)
# # 7 범죄 발생건수 8 범죄 발생건수/인구(명) 9 범죄 발생건수/인구밀도 10 범죄 발생건수/공무원 1인당 시민 수
# db_0 = c.fetchall()
# print(db_0)
#
# # 한글 폰트 사용을 위해서 세팅, 폰트 경로 설정
# font_path = "C:\\Windows\\Fonts\\gulim.ttc"
# # 폰트 패스를 통해 폰트 세팅해 폰트 이름 반환받아 font 변수에 삽입
# font = font_manager.FontProperties(fname=font_path).get_name()
# # 폰트 설정
# rc('font', family=font)
#
# # 변수 선언
# # 각 자치구별 현황
# dong_status = []
# seo_status = []
# nam_status = []
# book_status = []
# gwangsan_status = []
#
# # 각 자치구별 범죄 현황
# dong_crime = []
# seo_crime = []
# nam_crime = []
# book_crime = []
# gwangsan_crime = []
#
#
# # 구별 현황 삽입 함수, i=0~7까지
# def insert_status(goo_status, goo_number):
#     for i in range(8):
#         goo_status.append(db_0[goo_number][i])
#
#
# # 구별 변수 대비 범죄율 삽입 함수, i=8~10까지
# def insert_crime(goo_crime, goo_number):
#     for i in range(8, 11):
#         goo_crime.append(db_0[goo_number][i])
#
#
# def value_avg(goo_list, item_number):
#     result_avg = 0
#     for i in range(len(goo_list)):
#         result_avg += goo_list[i][item_number]
#     return result_avg / len(goo_list)
#
#
# # 함수를 실행해 각 리스트에 데이터 입력
# insert_status(dong_status, 0)
# insert_status(seo_status, 2)
# insert_status(nam_status, 1)
# insert_status(book_status, 4)
# insert_status(gwangsan_status, 3)
# insert_crime(dong_crime, 0)
# insert_crime(seo_crime, 2)
# insert_crime(nam_crime, 1)
# insert_crime(book_crime, 4)
# insert_crime(gwangsan_crime, 3)
#
# item_list = ['인구(명)', '인구밀도', '공무원 1인당 인구수', '인구 대비 범죄건수', '인구밀도 대비 범죄건수',
#              '공무원당 시민수 대비 범죄건수']


# ====================================================데이터 핸들링====================================================
# ==============================================인구 대비 범죄 건수 그래프==============================================

# # 그래프 제목
# plt.title('인구 대비 범죄건수')
# # 그래프 막대의 두께 설정
# bar_width = 0.35
# # 그래프의 x축을 담당할 라벨 설정
# goo_label = ['동구', '서구', '남구', '북구', '광산구']
# # 그래프 간격 설정
# space = np.arange(len(goo_label))
#
#
# plt.bar('동구', dong_crime[0], width=bar_width)
# plt.bar('서구', seo_crime[0], width=bar_width)
# plt.bar('남구', nam_crime[0], width=bar_width)
# plt.bar('북구', book_crime[0], width=bar_width)
# plt.bar('광산구', gwangsan_crime[0], width=bar_width)
#
# plt.show()

# ==============================================인구 대비 범죄 건수 그래프==============================================
# ============================================인구밀도 대비 범죄 건수 그래프============================================

# # 그래프 제목
# plt.title('인구밀도 대비 범죄건수')
# # 그래프 막대의 두께 설정
# bar_width = 0.35
# # 그래프의 x축을 담당할 라벨 설정
# goo_label = ['동구', '서구', '남구', '북구', '광산구']
# # 그래프 간격 설정
# space = np.arange(len(goo_label))
#
#
# plt.bar('동구', dong_crime[1], width=bar_width)
# plt.bar('서구', seo_crime[1], width=bar_width)
# plt.bar('남구', nam_crime[1], width=bar_width)
# plt.bar('북구', book_crime[1], width=bar_width)
# plt.bar('광산구', gwangsan_crime[1], width=bar_width)
#
# plt.show()

# ============================================인구밀도 대비 범죄 건수 그래프============================================
# ======================================공무원 1인당 인구수 대비 범죄 건수 그래프======================================

# # 그래프 제목
# plt.title('공무원 1인당 인구수 대비 범죄 건수')
# # 그래프 막대의 두께 설정
# bar_width = 0.35
# # 그래프의 x축을 담당할 라벨 설정
# goo_label = ['동구', '서구', '남구', '북구', '광산구']
# # 그래프 간격 설정
# space = np.arange(len(goo_label))
#
#
# plt.bar('동구', dong_crime[2], width=bar_width)
# plt.bar('서구', seo_crime[2], width=bar_width)
# plt.bar('남구', nam_crime[2], width=bar_width)
# plt.bar('북구', book_crime[2], width=bar_width)
# plt.bar('광산구', gwangsan_crime[2], width=bar_width)
#
#
# plt.show()

# ======================================공무원 1인당 인구수 대비 범죄 건수 그래프======================================

# c.execute('select a.`인구(명)`, round(`인구(명)`/`면적(제곱킬로미터)`) as "인구밀도(명/제곱킬로미터)",'
#           ' round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)",'
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` as "범죄 발생건수/인구(명)",'
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / round(`인구(명)`/`면적(제곱킬로미터)`)'
#           ' as "범죄 발생건수/인구밀도(명/km²)",'
#           ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / (`인구(명)`/`공무원(명)`)'
#           ' as "범죄 발생건수/공무원 1인당 시민 수"'
#           ' from `crime`.`광주광역시_자치구별 현황_20210731` as a'
#           ' inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b'
#           ' on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1) group by 관서명')
#
# db_1 = c.fetchall()
# print(db_1)
#
# item_list = ['인구(명)', '인구밀도', '공무원 1인당 인구수', '인구 대비 범죄건수', '인구밀도 대비 범죄건수',
#              '공무원당 시민수 대비 범죄건수']
#
# def total_status(goo_status, goo_number):
#     for i in range(6):
#         goo_status.append(db_1[goo_number][i])
#
# total_status(dong_status, 1)
# total_status(seo_status, 3)
# total_status(nam_status, 2)
# total_status(book_status, 5)
# total_status(gwangsan_status, 4)
# print(dong_status)
#
# # ======================================공무원 1인당 인구수 대비 범죄 건수 그래프======================================
#
# # 그래프 제목
# plt.title('공무원 1인당 인구수 대비 범죄 건수')
# # # 그래프 막대의 두께 설정
# bar_width = 0.35
#
# plt.bar(item_list, dong_status, width=bar_width)
# # plt.bar('서구', seo_crime[2], width=bar_width)
# # plt.bar('남구', nam_crime[2], width=bar_width)
# # plt.bar('북구', book_crime[2], width=bar_width)
# # plt.bar('광산구', gwangsan_crime[2], width=bar_width)
# #
# plt.show()

# ===================================================230104 test파일===================================================
# ===================================================230104 test파일===================================================
# ===================================================230104 test파일===================================================
# ===================================================230104 test파일===================================================
# ===================================================230104 test파일===================================================
# ===================================================230104 test파일===================================================

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
        self.elisa_list = []
        self.name=['광주북부경찰서','광주광산경찰서','광주서부경찰서','광주남부경찰서','광주동부경찰서']
        self.name2=['경찰서','발생건수', '검거건수', '검거인원', '구속', '불구속', '기타']
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
        sql = "Select * from `crime`.`category` limit 5"  # case2
        cur.execute(sql)
        self.a = cur.fetchall()

        # sql = "Select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`"#case1
        # DB에서 경찰서명, 인구수(만명)
        elisa_sql = ('select c.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", '
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
                for j in range(7):
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
