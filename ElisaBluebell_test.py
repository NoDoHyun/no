# # =======================================================설정=======================================================

# DB 사용을 위해 세팅
import pymysql
# 그래프를 그리기 위해 세팅
import matplotlib.pyplot as plt
import numpy as np
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
#
# # =======================================================설정=======================================================
# # ===================================================데이터 핸들링===================================================

# mysql 로그인 및 db 획득
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

# 커서 지정
c = conn.cursor()

# 발생건수 테스트 출력
# c.execute('select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` where 구분="발  생  건  수"')
# a = c.fetchall()
# print(a)
# c.execute('select * from `crime`.`광주광역시_CCTV_20220429`')
# a = c.fetchall()
# print(a)
# crime 스키마 내에서 경찰서, 인구,
c.execute('select c.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", '
          # 범죄 발생 건수
          'b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수, '
          # 5대범죄 발생 건수 / (인구 * 10,000) = 인구 1만명당 범죄 발생 건수
          'round((b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` * 10000) '
          'as "인구 1만명당 범죄 건수", '
          # 5대 범죄 발생 건수 / 면적 = 면적당 범죄 발생 건수
          '(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / `면적(제곱킬로미터)` as "범죄 건수/면적(km²)", '
          # 검거 건수와 검거율(검거 건수 / 범죄 발생 건수)
          'c.검거건수, c.검거건수/(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) * 100 as "검거율(%)", '
          # CCTV 대수와 인구 / CCTV 1대당 인구수를 셀렉(18이 어디선가 곱해져서 18로 나눔. 해결 방법은 찾아두었으나
          # 다른 문제가 발생하여 임시로 보류)
          'round(sum(d.카메라대수)/18) as 카메라대수, a.`인구(명)`/(sum(d.카메라대수)/18) as "카메라 1대당 인구수" '
          # 자치구별 현황 테이블
          'from `crime`.`광주광역시_자치구별 현황_20210731` as a '
          # 자치구별 5대 범죄 현황 테이블
          'inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b '
          # 카테고리(범죄 현황 요약) 테이블
          'inner join `crime`.`category` as c '
          # 광주시 CCTV 설치 정보 테이블 조인
          'inner join `crime`.`광주광역시_cctv_20220429` as d '
          # 광주광역시 <남>구 등 7번째 1글자 = 광주<남>부 등 3번째 1글자일 때, 이하 동일
          'on mid(d.소재지지번주소, 7, 1) = mid(c.경찰서, 3, 1) '
          'on mid(c.경찰서, 3, 1) = mid(b.관서명, 3, 1) '
          'on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1) '
          # 관서명으로 묶고 범죄발생건수로 나열하여 광주<광>역시경찰청 제외하고 출력
          'group by 관서명 order by 범죄발생건수 limit 1, 5')

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

# 그래프 제목
plt.title('공무원 1인당 인구수 대비 범죄 건수')
# # 그래프 막대의 두께 설정
bar_width = 0.35

plt.bar(item_list, dong_status, width=bar_width)
# plt.bar('서구', seo_crime[2], width=bar_width)
# plt.bar('남구', nam_crime[2], width=bar_width)
# plt.bar('북구', book_crime[2], width=bar_width)
# plt.bar('광산구', gwangsan_crime[2], width=bar_width)
#
plt.show()

