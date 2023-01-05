# 프로그램 온오프를 위해 추가
import sys
# DB 사용을 위해 세팅
import pymysql
# 그래프를 그리기 위해 세팅
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import numpy as np
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc


# 각 구의 현황판 작성을 위한 페이지
class CrimeTablePage(QWidget):
    def __init__(self):
        super().__init__()
        # 변수 선언
        self.db_average = ['평균', 0, 0, 0, 0, 0, 0, 0, 0]
        self.dongboo = []
        self.seoboo = []
        self.namboo = []
        self.bookboo = []
        self.gwangsan = []
        # 창 설정
        self.setGeometry(0, 0, 1024, 768)
        # db 세팅
        self.load_db()
        self.set_db()
        self.set_table()
        self.set_btn()

        # 버튼 클릭시 각 매서드 이동
        self.dongboo_btn.clicked.connect(self.dongboograph)
        self.seoboo_btn.clicked.connect(self.seoboograph)
        self.bookboo_btn.clicked.connect(self.bookboograph)
        self.namboo_btn.clicked.connect(self.namboograph)
        self.gwangsan_btn.clicked.connect(self.gwangsangraph)

        self.graph_list=[]

    def dongboograph(self):
        self.graph(k=0)

    def namboograph(self):
        self.graph(k=1)

    def seoboograph(self):
        self.graph(k=2)

    def gwangsangraph(self):
        self.graph(k=3)

    def bookboograph(self):
        self.graph(k=4)

    def graph_ready(self):
        # 그래프에 사용하기 좋게 데이터 리스트화
        self.graph_list.clear()
        temp=list(self.db)
        for i in temp:
            self.graph_list.append(list(i))

        # 관서명 삭제 : 각 리스트 [0] 삭제
        for i in range(len(self.graph_list)):
            del self.graph_list[i][0]

        # 마지막 리스트에 관서명 넣기
        self.graph_list.insert(6,['동부','남부','서부','광산','북부'])

    # 0.동부 1.남부 2.서부 3.광산 4.북부
    def graph(self,k):
        self.graph_ready()
        # 그래프 기본 스타일 설정
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 9)
        plt.rcParams['font.size'] = 10
        font_path = "C:\\Windows\\Fonts\\gulim.ttc"
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)

        # 그래프 데이터 준비
        x = np.arange(4)
        data = (['인구(만명)', '범죄건수(만명)', '검거율(%)', '카메라당인구(만명)'])
        y1 = np.array([self.db_average[1], self.db_average[3], self.db_average[6], self.db_average[8]])
        y2 = np.array([self.graph_list[k][0], self.graph_list[k][2], self.graph_list[k][5], self.graph_list[k][7]])

        # 그래프 그리기
        fig, ax1 = plt.subplots()

        ax1.plot(x, y1, color='green', markersize=7, linewidth=5, alpha=0.7, label='구 전체평균')
        ax1.set_ylim(0, 350)
        ax1.set_xlabel('요소')
        ax1.set_ylabel('구 전체평균')

        ax2 = ax1.twinx()
        ax2.bar(x, y2, color='deeppink', label='요소별 값', alpha=0.7, width=0.7)
        ax2.set_ylim(0, 350)
        ax2.set_ylabel(r'요소별 값')

        ax1.set_zorder(ax2.get_zorder() + 10)
        ax1.patch.set_visible(False)

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.title(f'{self.graph_list[5][k]} 요소별 구 전체평균과 비교')
        plt.xticks(x, data)

        plt.show()

    # 테이블 위젯 생성
    def set_table(self):
        self.crime_table = QTableWidget(self)
        self.crime_table.setRowCount(6)
        self.crime_table.setColumnCount(9)
        self.crime_table.setGeometry(140, 230, 790, 400)
        self.crime_table.setHorizontalHeaderLabels(['구분', '인구(만명)', '범죄건수', '인구 1만명당 범죄건수', '범죄 건수(km²)',
                                               '검거건수', '검거율(%)', '카메라 대수', '카메라당 인구수(만명)'])
        self.crime_table.setColumnWidth(0, 91)
        self.crime_table.setColumnWidth(1, 64)
        self.crime_table.setColumnWidth(2, 56)
        self.crime_table.setColumnWidth(3, 131)
        self.crime_table.setColumnWidth(4, 91)
        self.crime_table.setColumnWidth(5, 56)
        self.crime_table.setColumnWidth(6, 63)
        self.crime_table.setColumnWidth(7, 72)
        self.crime_table.setColumnWidth(8, 128)
        self.crime_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.crime_table.verticalHeader().setVisible(False)
        self.crime_table.isSortingEnabled()
        self.set_table_data()

    def set_table_data(self):
        for i in range(len(self.db)):
            for j in range(len(self.db[0])):
                self.crime_table.setItem(i, j, QTableWidgetItem(str(self.db[i][j])))
        for i in range(len(self.db_average)):
            self.crime_table.setItem(5, i, QTableWidgetItem(str(self.db_average[i])))

    def set_btn(self):
        self.dongboo_btn = QPushButton('동부경찰서', self)
        self.seoboo_btn = QPushButton('서부경찰서', self)
        self.bookboo_btn = QPushButton('북부경찰서', self)
        self.namboo_btn = QPushButton('남부경찰서', self)
        self.gwangsan_btn = QPushButton('광산경찰서', self)
        self.dongboo_btn.setGeometry(10, 10, 80, 50)
        self.seoboo_btn.setGeometry(110, 110, 80, 50)
        self.namboo_btn.setGeometry(210, 210, 80, 50)
        self.bookboo_btn.setGeometry(310, 310, 80, 50)
        self.gwangsan_btn.setGeometry(41, 410, 80, 50)


    # db 호출 함수
    def load_db(self):
        # mysql 로그인 및 db 획득
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='crime')

        # 커서 지정
        c = conn.cursor()
        c.execute('select c.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", '
                  # 범죄 발생 건수
                  'b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수, '
                  # 5대범죄 발생 건수 / (인구 * 10,000) = 인구 1만명당 범죄 발생 건수
                  'round((b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` * 10000) '
                  'as "인구 1만명당 범죄 건수", '
                  # 5대 범죄 발생 건수 / 면적 = 면적당 범죄 발생 건수
                  '(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / `면적(제곱킬로미터)` as "범죄 건수/면적(km²)", '
                  # 검거 건수와 검거율(검거 건수 / 범죄 발생 건수)
                  'c.검거건수, c.검거건수/(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도)*100 as "검거율(%)", '
                  # CCTV 대수와 인구 / 인구 1만명당 카메라 수를 셀렉
                  'round(sum(d.카메라대수)/6) as 카메라대수, (sum(d.카메라대수)/6)/a.`인구(명)`*10000 '
                  'as "1만명당 카메라 수" '
                  # 자치구별 현황 테이블
                  'from `crime`.`광주광역시_자치구별 현황_20210731` as a '
                  # 자치구별 5대 범죄 현황 테이블 조인
                  'inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b '
                  # 카테고리(범죄 현황 요약) 테이블 조인
                  'inner join `crime`.`category` as c '
                  # 광주시 CCTV 설치 정보 테이블 조인
                  'inner join `crime`.`광주광역시_cctv_20220429` as d '
                  # 광주광역시 <남>구 등 7번째 1글자 = 광주<남>부 등 3번째 1글자일 때, 이하 동일
                  'on mid(d.소재지지번주소, 7, 1) = mid(c.경찰서, 3, 1) '
                  'on mid(c.경찰서, 3, 1) = mid(b.관서명, 3, 1) '
                  'on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1) '
                  # 관서명으로 묶고 범죄발생건수로 나열하여 광주<광>역시경찰청 제외하고 출력
                  'group by 관서명, 경찰서 order by 범죄발생건수 limit 1, 5')
        # 불러온 모든 값을 db 변수에 삽입
        self.db = c.fetchall()
        # 커서와 커넥션 닫음
        c.close()
        conn.close()

    # db 설정 함수
    def set_db(self):
        # 각 관할 경찰서 db 설정
        self.dongboo = self.db[0]
        self.namboo = self.db[1]
        self.seoboo = self.db[2]
        self.gwangsan = self.db[3]
        self.bookboo = self.db[4]
        # 평균값 생성 함수 호출
        self.set_average()

    # 평균값 생성 함수
    def set_average(self):
        # load_db 함수에서 불러온 db의 행만큼 반복
        for i in range(len(self.db)):
            # db의 열만큼 반복하나 첫번째는 각 관할 경찰서 명이 들어갔으므로 제외하기 위해 1부터 시작
            for j in range(1, len(self.db[0])):
                # i행(관할 경찰서)의 j번째(각 항목) 값들을 평균값 리스트의 j번째 항목에 더해줌
                self.db_average[j] += self.db[i][j]
        # 평균값 리스트의 열의 갯수만큼 반복, 위와 같이 첫번째에는 '평균'이라는 문자열이 들어갔으므로 1부터 시작함
        for i in range(1, len(self.db_average)):
            # 각 열을 받아온 db의 행의 갯수로 나누어 평균을 구함
            self.db_average[i] /= len(self.db)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CrimeTablePage()
    ex.show()
    app.exec_()
