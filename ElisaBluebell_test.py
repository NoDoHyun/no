# -*- coding: utf-8 -*-
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
        self.insert_dialog = InsertDialog()
        self.db = []
        self.selected_row = []
        self.db_average = ['평균', 0, 0, 0, 0, 0, 0, 0, 0]
        self.dongboo = []
        self.seoboo = []
        self.namboo = []
        self.bookboo = []
        self.gwangsan = []
        self.cctv_db = []
        # 창 설정
        self.setGeometry(0, 0, 1024, 768)
        # db 세팅
        self.load_db()
        self.set_db()
        # ui 세팅
        self.set_label()
        self.set_table1()
        self.set_table2()
        self.set_line()
        self.set_btn()
        self.graph_list = []
        # 버튼 클릭시 각 매서드 이동
        self.dongboo_btn.clicked.connect(self.dongboograph)
        self.seoboo_btn.clicked.connect(self.seoboograph)
        self.bookboo_btn.clicked.connect(self.bookboograph)
        self.namboo_btn.clicked.connect(self.namboograph)
        self.gwangsan_btn.clicked.connect(self.gwangsangraph)

    # db 호출 함수
    def load_db(self):
        # mysql 로그인 및 db 획득
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='crime')
        # 커서 지정
        c = conn.cursor()
        # 경찰서, 인구, 발생건수
        c.execute('select b.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", b.발생건수, '
                  # 발생건수 / 인구 * 10,000 = 인구 10,000명당 범죄율
                  'round((b.발생건수) / a.`인구(명)` * 10000) as "인구 1만명당 범죄 건수", '
                  # 발생건수 / km² = 면적대비 범죄율
                  '(b.발생건수) / `면적(제곱킬로미터)` as "범죄 건수/면적(km²)", '
                  # 검거건수, 검거건수 / 발생건수 = 검거율
                  'b.검거건수, b.검거건수/b.발생건수 * 100 as "검거율(%)", '
                  # CCTV 갯수
                  'round(sum(c.카메라대수)) as "CCTV 갯수", '
                  # CCTV 갯수 / 인구 * 1,000 = 1,000명당 CCTV 수
                  'sum(c.카메라대수)/a.`인구(명)`*1000 as "1천명당 CCTV 수" '
                  # 광주광역시 현황 테이블을 a로 받아옴
                  'from `crime`.`광주광역시_자치구별 현황_20210731` as a '
                  # 범죄 종합 테이블을 b로 선언하며 조인
                  'inner join `crime`.`category` as b '
                  # CCTV 정보를 c로 선언하며 조인
                  'inner join `crime`.`광주광역시_cctv_20220429` as c '
                  # 주소와 경찰서명간 같은 단어(동서남북광)로 엮음
                  'on mid(c.소재지지번주소, 7, 1) = mid(b.경찰서, 3, 1) '
                  # 경찰서와 구 명칭 중 같은 단어로 엮음
                  'on mid(a.구분, 7, 1) = mid(b.경찰서, 3, 1) '
                  # 경찰서로 그룹화하여 발생건수 오름차순으로 나열
                  'group by 경찰서, 구분 order by 발생건수')
        # 불러온 모든 값을 db 변수에 삽입
        self.db = c.fetchall()
        # cctv 테이블 호출
        c.execute('select * from `crime`.`광주광역시_cctv_20220429`')
        # 임시값에 내용 저장
        temp = c.fetchall()
        # 길이가 5 미만일 경우(아직 삭제여부가 생성되지 않았을 경우)
        if len(temp[0]) < 5:
            # cctv.db에 모든 내용 삽입
            for i in range(len(temp)):
                self.cctv_db.append(temp[i])
        # 길이가 5 이상인 경우
        else:
            for i in range(len(temp)):
                # 불러온 데이터에서 삭제여부가 Y가 아닐 때에만 self.cctv_db에 내용 삽입
                if temp[i][4] != 'Y':
                    self.cctv_db.append(temp[i])
        # 커서와 커넥션 닫음
        c.close()
        conn.close()

    # DB 설정 함수
    def set_db(self):
        # 각 관할 경찰서 db 설정
        self.dongboo = self.db[0]
        self.namboo = self.db[1]
        self.seoboo = self.db[2]
        self.gwangsan = self.db[3]
        self.bookboo = self.db[4]
        # 평균값 생성 함수 호출
        self.set_average()

    # 라인에딧 설정
    def set_line(self):
        # 검색을 위한 라인에딧 설정함
        self.search_line = QLineEdit(self)
        self.search_line.setGeometry(190, 380, 200, 20)
        # 검색창 엔터시 검색 기능 실행
        self.search_line.returnPressed.connect(self.table2_search)

    # 버튼 세팅 함수
    def set_btn(self):
        self.dongboo_btn = QPushButton('동부경찰서\n현황그래프', self)
        self.seoboo_btn = QPushButton('서부경찰서\n현황그래프', self)
        self.bookboo_btn = QPushButton('북부경찰서\n현황그래프', self)
        self.namboo_btn = QPushButton('남부경찰서\n현황그래프', self)
        self.gwangsan_btn = QPushButton('광산경찰서\n현황그래프', self)
        self.go_back_btn = QPushButton('돌아가기', self)
        self.search_btn = QPushButton('검색', self)
        self.delete_btn = QPushButton('삭제', self)
        self.save_btn = QPushButton('저장', self)
        self.insert_btn = QPushButton('추가', self)
        self.dongboo_btn.setGeometry(130, 700, 78, 43)
        self.seoboo_btn.setGeometry(230, 700, 78, 43)
        self.namboo_btn.setGeometry(330, 700, 78, 43)
        self.bookboo_btn.setGeometry(430, 700, 78, 43)
        self.gwangsan_btn.setGeometry(530, 700, 78, 43)
        self.go_back_btn.setGeometry(804, 700, 78, 43)
        self.search_btn.setGeometry(410, 380, 40, 20)
        self.save_btn.setGeometry(465, 380, 40, 20)
        self.delete_btn.setGeometry(520, 380, 40, 20)
        self.insert_btn.setGeometry(575, 380, 40, 20)
        # 버튼 스위치
        # 검색 버튼 클릭시 검색 기능 실행
        self.search_btn.clicked.connect(self.table2_search)
        self.save_btn.clicked.connect(self.save_db)
        self.delete_btn.clicked.connect(self.table2_delete_item)
        self.go_back_btn.clicked.connect(self.go_back)
        self.insert_btn.clicked.connect(self.popup_insert_dialog)

    # 라벨 세팅
    def set_label(self):
        from PyQt5.QtCore import Qt
        self.table1_label = QLabel('광주광역시 종합현황표', self)
        self.table2_label = QLabel('CCTV 종합정보', self)
        self.search_label = QLabel('주소 입력', self)
        self.table1_label.setGeometry(0, 40, 1024, 20)
        self.table2_label.setGeometry(0, 345, 1024, 20)
        self.search_label.setGeometry(130, 380, 60, 20)
        self.table1_label.setAlignment(Qt.AlignCenter)
        self.table2_label.setAlignment(Qt.AlignCenter)

    # CCTV 정보 추가 새 창 출력
    def popup_insert_dialog(self):
        self.insert_dialog.show()

    def go_back(self):
        self.parent().setCurrentIndex(0)

    def dongboograph(self):
        self.graph(0)

    def namboograph(self):
        self.graph(1)

    def seoboograph(self):
        self.graph(2)

    def gwangsangraph(self):
        self.graph(3)

    def bookboograph(self):
        self.graph(4)

    def graph_ready(self):
        # 그래프에 사용하기 좋게 데이터 리스트화
        self.graph_list.clear()
        temp = list(self.db)
        for i in temp:
            self.graph_list.append(list(i))

        # 관서명 삭제 : 각 리스트 [0] 삭제
        for i in range(len(self.graph_list)):
            del self.graph_list[i][0]

        # 마지막 리스트에 관서명 넣기
        self.graph_list.insert(6, ['동부', '남부', '서부', '광산', '북부'])

    # 0.동부 1.남부 2.서부 3.광산 4.북부
    def graph(self, k):
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
        data = (['인구(만명)', '범죄건수(만명)', '검거율(%)', '인구당 CCTV 수(1,000명/개)'])
        y1 = np.array([self.db_average[1], self.db_average[3], self.db_average[6], self.db_average[8]])
        y2 = np.array([self.graph_list[k][0], self.graph_list[k][2], self.graph_list[k][5], self.graph_list[k][7]])

        # 그래프 그리기
        fig, ax1 = plt.subplots()

        ax1.plot(x, y1, color='green', markersize=7, linewidth=5, alpha=0.7, label='광주시 평균')
        ax1.set_ylim(0, 130)
        ax1.set_xlabel('요소')
        ax1.set_ylabel('구 전체평균')

        ax2 = ax1.twinx()
        ax2.bar(x, y2, color='deeppink', label=self.graph_list[5][k], alpha=0.7, width=0.7)
        ax2.set_ylim(0, 130)
        ax1.set_zorder(ax2.get_zorder() + 10)
        ax1.patch.set_visible(False)

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.title(f'{self.graph_list[5][k]} 요소별 구 전체평균과 비교')
        plt.xticks(x, data)

        plt.show()

    # 종합정보 테이블 위젯 생성
    def set_table1(self):
        self.crime_table = QTableWidget(self)
        # 5개구 경찰서와 평균 총 6줄 필요
        self.crime_table.setRowCount(6)
        # 아래 칼럼 라벨 설정한 9개의 항목 출력 필요
        self.crime_table.setColumnCount(9)
        self.crime_table.setGeometry(130, 100, 754, 205)
        self.crime_table.setHorizontalHeaderLabels(['구분', '인구(만명)', '범죄건수', '인구 1만명당 범죄건수',
                                                    '범죄 건수(km²)', '검거건수', '검거율(%)', 'CCTV 대수',
                                                    '1천명당 CCTV 수'])
        # 각 열의 크기는 내용과 제목의 출력에 맞춤
        self.crime_table.setColumnWidth(0, 91)
        self.crime_table.setColumnWidth(1, 64)
        self.crime_table.setColumnWidth(2, 56)
        self.crime_table.setColumnWidth(3, 131)
        self.crime_table.setColumnWidth(4, 91)
        self.crime_table.setColumnWidth(5, 56)
        self.crime_table.setColumnWidth(6, 63)
        self.crime_table.setColumnWidth(7, 72)
        self.crime_table.setColumnWidth(8, 128)
        # 클릭을 통한 수정 불가능
        self.crime_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 버티칼 헤더 적용 안함
        self.crime_table.verticalHeader().setVisible(False)
        # 종합정보표 데이터 세팅 함수 호출
        self.set_table1_data()

    # 종합정보표
    def set_table1_data(self):
        for i in range(len(self.db)):
            for j in range(len(self.db[0])):
                # 현재 값이 문자열이 아닐 때
                if type(self.db[i][j]) != str:
                    # 소수점 값을 가지고 있다면
                    if float(self.db[i][j]) - int(self.db[i][j]) > 0:
                        # 4개의 숫자만 표에 입력, DB에서 바로 받아와서 튜플값이기 때문에 입력을 별개로 해줌.
                        self.crime_table.setItem(i, j, QTableWidgetItem(str(f'{self.db[i][j]:.4}')))
                    # 아니면 그냥 입력
                    else:
                        self.crime_table.setItem(i, j, QTableWidgetItem(str(self.db[i][j])))
                else:
                    self.crime_table.setItem(i, j, QTableWidgetItem(str(self.db[i][j])))
        for i in range(len(self.db_average)):
            # 위와는 다른 방법으로 파이썬의 특권을 누려보기 위해 사용해봄, 4열 6열 8열은
            if i == 4 or i == 6 or i == 8:
                # 숫자를 4개만 출력
                self.crime_table.setItem(5, i, QTableWidgetItem(str(f'{self.db_average[i]:.4}')))
            # 아님 말고
            else:
                self.crime_table.setItem(5, i, QTableWidgetItem(str(self.db_average[i])))

    # cctv 정보 확인을 위한 2번째 테이블 작성
    def set_table2(self):
        self.cctv_table = QTableWidget(self)
        # cctv_db 튜플의 길이만큼 행 설정
        self.cctv_table.setRowCount(len(self.cctv_db))
        # CCTV 정보 표시를 위한 4개의 열을 가짐
        self.cctv_table.setColumnCount(4)
        # 표의 크기는 종합정보표와 같음
        self.cctv_table.setGeometry(130, 405, 754, 205)
        self.cctv_table.setHorizontalHeaderLabels(['CCTV 대수', '관리기관명', '소재지도로명주소', '소재지지번주소'])
        # 1열과 2열은 헤더와 내용을 출력하기에 부족함이 없게, 나머지 3, 4열에 분배
        self.cctv_table.setColumnWidth(0, 72)
        self.cctv_table.setColumnWidth(1, 131)
        self.cctv_table.setColumnWidth(2, 266)
        self.cctv_table.setColumnWidth(3, 266)
        # 버티컬헤더 없음
        self.cctv_table.verticalHeader().setVisible(False)
        # cctv_db에서 받아온 데이터를 표에 입력해주는 함수 호출
        self.set_table2_data()
        self.cctv_table.clicked.connect(self.save_data)

    # 얘가 그 함수임
    def set_table2_data(self):
        # 단순 반복 입력
        for i in range(len(self.cctv_db)):
            # 단순 반복 입력이었으나 db 순서가 꼬여 원하는대로 칼럼을 맞춰주기위해 수동으로 칼럼 설정
            self.cctv_table.setItem(i, 0, QTableWidgetItem(str(self.cctv_db[i][3])))
            self.cctv_table.setItem(i, 1, QTableWidgetItem(str(self.cctv_db[i][0])))
            self.cctv_table.setItem(i, 2, QTableWidgetItem(str(self.cctv_db[i][1])))
            self.cctv_table.setItem(i, 3, QTableWidgetItem(str(self.cctv_db[i][2])))

    def table2_delete_item(self):
        # 삭제여부 재확인
        reply = QMessageBox.question(self, '삭제', '삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        # yes 선택시 삭제 프로세스 진행
        if reply == QMessageBox.Yes:
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='crime')
            c = conn.cursor()
            # 삭제 처음 실행시
            if len(self.cctv_db[0]) < 5:
                # 테이블에 삭제여부 행 추가함
                c.execute('alter table `crime`.`광주광역시_cctv_20220429` add column 삭제여부 text after 카메라대수')
                # 모든 데이터의 삭제여부 행에 N값 넣어줌
                c.execute('update `crime`.`광주광역시_cctv_20220429` set 삭제여부="N"')
            # 데이터 삭제를 위해 선택된 행의 지번주소 받아옴(도로명 주소는 생략된 경우 있음)
            adress = self.cctv_db[self.cctv_table.currentRow()][2]
            # DB상 소재지지번주소가 선택된 행의 지번주소와 같은 행을 찾아 삭제여부를 Y로 변경함
            c.execute(f'update `crime`.`광주광역시_cctv_20220429` set 삭제여부="Y" where 소재지지번주소="{adress}"')
            # 커밋을 해서 변경내용 적용
            conn.commit()
            # 커서와 커넥션 닫음
            c.close()
            conn.close()
            # 표 재출력을 위해 cctv_db 리스트 초기화
            self.cctv_db.clear()
            # db 리로드
            self.load_db()
            # cctv 표 검색 재실행
            self.table2_search()
        else:
            pass

    # 수정을 위한 선택행 저장 함수
    def save_data(self):
        if self.cctv_table.currentRow() not in self.selected_row:
            self.selected_row.append(self.cctv_table.currentRow())

    # 데이터 저장
    def save_db(self):
        # self.selected_row에 내용이 있는 경우 반복함
        reply = QMessageBox.question(self, '저장', '저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        # 예 누를 시 데이터 저장
        if reply == QMessageBox.Yes:
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='crime')
            c = conn.cursor()
            while self.selected_row:
                # 데이터 리스트에 각각의 변경된 값 적용
                c.execute(f'''update `crime`.`광주광역시_cctv_20220429` 
                set 카메라대수={int(self.cctv_table.item(self.selected_row[0], 0).text())} ,
                관리기관명="{self.cctv_table.item(self.selected_row[0], 1).text()}", 
                소재지도로명주소="{self.cctv_table.item(self.selected_row[0], 2).text()}", 
                소재지지번주소="{self.cctv_table.item(self.selected_row[0], 3).text()}" 
                where 소재지지번주소="{self.cctv_db[self.selected_row[0]][2]}"''')
                conn.commit()
                # 적용한 업체를 리스트에서 제거
                self.selected_row.remove(self.selected_row[0])
            c.close()
            conn.close()
            # 표 재출력을 위해 cctv_db 리스트 초기화
            self.cctv_db.clear()
            # db 리로드
            self.load_db()
            # cctv 표 검색 재실행
            self.table2_search()

    # 데이터 검색 함수
    def table2_search(self):
        # 검색에 활용할 리스트 선언
        search_result = []
        # cctv_db와 테이블 리셋
        self.cctv_db.clear()
        self.load_db()
        self.cctv_table.clear()
        # cctv_table 라벨 설정
        self.cctv_table.setHorizontalHeaderLabels(['CCTV 대수', '관리기관명', '소재지도로명주소', '소재지지번주소'])
        # 도로명 주소와 지번 주소 중 lineedit text와 일치하는 내역이 있는지 확인(관리기관은 전부 동일하므로 검색 제외)
        for i in range(len(self.cctv_db)):
            if self.search_line.text() in self.cctv_db[i][1] or self.search_line.text() in self.cctv_db[i][2]:
                search_result.append(self.cctv_db[i])
        # cctv_db 리스트의 길이만큼 행 설정
        self.cctv_table.setRowCount(len(search_result))
        for i in range(len(search_result)):
            # table2 DB와 칼럼 순서를 일치시키기 위해 수도
            self.cctv_table.setItem(i, 0, QTableWidgetItem(str(search_result[i][3])))
            self.cctv_table.setItem(i, 1, QTableWidgetItem(str(search_result[i][0])))
            self.cctv_table.setItem(i, 2, QTableWidgetItem(str(search_result[i][1])))
            self.cctv_table.setItem(i, 3, QTableWidgetItem(str(search_result[i][2])))
        # 수정에서 사용하기 위해 cctv_db에 실제 표에 삽입된 데이터를 넣음
        self.cctv_db = search_result

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


# 데이터 추가용 다이얼로그
class InsertDialog(QWidget):

    def __init__(self):
        super().__init__()
        # 창 크기 설정
        self.setGeometry(300, 150, 200, 250)
        # ui 세팅
        self.set_label()
        self.set_btn()
        self.set_line()
        self.set_combo()

    # 라벨 세팅
    def set_label(self):
        # 라벨 텍스트 중앙 정렬을 위한 Qt 로컬 호출
        from PyQt5.QtCore import Qt
        self.title_label = QLabel('CCTV 설치 현황 추가', self)
        self.street_label = QLabel('도로명주소', self)
        self.legacy_label = QLabel('지번주소', self)
        self.cctv_label = QLabel('CCTV 설치 대수', self)
        self.title_label.setGeometry(0, 20, 200, 20)
        self.street_label.setGeometry(0, 50, 200, 20)
        self.legacy_label.setGeometry(0, 100, 200, 20)
        self.cctv_label.setGeometry(0, 150, 200, 20)
        # 라벨 텍스트 가운데 정렬
        self.title_label.setAlignment(Qt.AlignCenter)
        self.street_label.setAlignment(Qt.AlignCenter)
        self.legacy_label.setAlignment(Qt.AlignCenter)
        self.cctv_label.setAlignment(Qt.AlignCenter)

    # 콤보박스 세팅
    def set_combo(self):
        self.cctv_combo = QComboBox(self)
        self.cctv_combo.setGeometry(70, 170, 60, 20)
        # 콤보박스에 표시될 숫자와 데이터 삽입
        for i in range(1, 10):
            self.cctv_combo.addItem(str(i), i)

    # 라인에딧 세팅
    def set_line(self):
        self.street_adress = QLineEdit(self)
        self.legacy_adress = QLineEdit(self)
        self.street_adress.setGeometry(20, 70, 160, 20)
        self.legacy_adress.setGeometry(20, 120, 160, 20)

    # 버튼 세팅
    def set_btn(self):
        self.go_back_btn = QPushButton('닫기', self)
        self.insert_btn = QPushButton('추가', self)
        self.go_back_btn.setGeometry(110, 220, 40, 20)
        self.insert_btn.setGeometry(50, 220, 40, 20)
        self.go_back_btn.clicked.connect(self.close_dialog)
        self.insert_btn.clicked.connect(self.insert_data)

    # 닫기 버튼 클릭시 다이얼로그 닫힘
    def close_dialog(self):
        self.close()

    # 추가 버튼 클릭시 데이터 추가함
    def insert_data(self):
        # 데이터 추가를 위한 로컬 import
        import pymysql
        # DB 커넥트
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='crime')
        # 커서 지정
        c = conn.cursor()
        # 지번주소가 비어있을 경우
        if not self.legacy_adress.text():
            # 경고창 출력
            warn = QMessageBox.warning(self, '주소 입력', '지번 주소를 입력해주세요.')
        # 지번주소가 입력된 경우
        else:
            # 입력된 데이터를 DB에 입력
            c.execute(f'''insert into `crime`.`광주광역시_cctv_20220429` (관리기관명, 소재지도로명주소, 소재지지번주소,
             카메라대수) values ("광주광역시 사회재난과", "{self.street_adress.text()}", "{self.legacy_adress.text()}"
             , {self.cctv_combo.currentData()})''')
            # 커밋
            conn.commit()
            # 중복 입력 방지를 위한 알림창 출력
            complete = QMessageBox.information(self, '추가 성공', 'CCTV 정보가 등록되었습니다.')
        # 커서와 커넥션 닫음
        c.close()
        conn.close()
