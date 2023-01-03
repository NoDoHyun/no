import sys
# DB 사용을 위해 세팅
import pymysql
# 그래프를 그리기 위해 세팅
import matplotlib.pyplot as plt
import numpy as np
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
from PyQt5.QtWidgets import *

# mysql 로그인 및 db 획득
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

# 커서 지정
c = conn.cursor()

# # 발생건수 테스트 출력
# c.execute('select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` where 구분="발  생  건  수"')
# a = c.fetchall()
# print(a)
# c.execute('select * from `crime`.`광주광역시_CCTV_20220429`')
# a = c.fetchall()
# print(a)
# crime 스키마 내의 광주광역시 자치구별 현황 테이블에서 구분, 세대수, 인구, 공무원, 면적 불러옴
c.execute('select a.구분, a.세대수, a.`인구(명)`, a.`공무원(명)`, a.`면적(제곱킬로미터)`,'
          # 공무원 1인당 인구 산출
          ' round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)",'
          # 인구밀도 산출
          ' round(`인구(명)`/`면적(제곱킬로미터)`) as "인구밀도(명/제곱킬로미터)",'
          # 범죄 발생 건수 산출
          ' b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수,'
          # 인구수 대비 범죄율 산출
          ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` as "범죄 발생건수/인구(명)",'
          # 인구밀도 대비 범죄율 산출
          ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / round(`인구(명)`/`면적(제곱킬로미터)`)'
          ' as "범죄 발생건수/인구밀도(명/km²)",'
          # 공무원당 담당 인구수 대비 범죄율
          ' (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / (`인구(명)`/`공무원(명)`)'
          ' as "범죄 발생건수/공무원 1인당 시민 수"'
          # 자치구별 현황을 a로 받아옴
          'from `crime`.`광주광역시_자치구별 현황_20210731` as a'
          # 자치구별 5대 범죄 현황을 b로 받아와서 조인
          ' inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b'
          # 각 구와 경찰서의 명칭 중 동서남북광이 겹치는 것을 매개로 연결
          ' on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1)'
          # 관서명으로 묶어 범죄발생건수(맨 위에 나옴) 제외한 나머지 값 표시제거 
          ' group by 관서명'
          # 범죄발생건수 오름차순 정렬해서 관할구가 존재하지 않는 시 경찰청을 맨 위로 올림
          ' order by 범죄발생건수'
          # 1번째 순서를 제외한 5개 출력으로 시 경찰청 제외한 나머지 출력 
          ' limit 1, 5')

#
a = c.fetchall()
print(a[0][8])

# 한글 폰트 사용을 위해서 세팅, 폰트 경로 설정
font_path = "C:\\Windows\\Fonts\\gulim.ttc"
# 폰트 패스를 통해 폰트 세팅해 폰트 이름 반환받아 font 변수에 삽입
font = font_manager.FontProperties(fname=font_path).get_name()
# 폰트 설정
rc('font', family=font)

# 그래프 제목
plt.title('광주광역시 자치구별 현황')
# 그래프 막대의 두께 설정
bar_width = 0.1
# 그래프의 x축을 담당할 라벨 설정
label = ['동구', '서구', '남구', '북구', '광산구']
# 그래프 간격 설정
space = np.arange(len(label))

# 막대그래프 생성
# plt.bar(space, tips_sum_by_day)

plt.bar(['광산구', '북구', '서구', '동구'], [10, 20, 30, 40], label='커짐', width=bar_width)
# plt.bar(bar_width + 1, [20, 30, 40, 10], label='', width=bar_width)
plt.legend()
plt.show()
