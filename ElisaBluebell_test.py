import sys
import matplotlib.pyplot as plt
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
import pymysql
from PyQt5.QtWidgets import *

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

c = conn.cursor()

bar_width = 0.1

font_path = "C:\\Windows\\Fonts\\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

plt.title('plotting')

plt.bar(['광산구', '북구', '서구', '동구'], [10, 20, 30, 40], label='커짐', width=bar_width)
# plt.bar(bar_width + 1, [20, 30, 40, 10], label='', width=bar_width)
plt.legend()
plt.show()
