import sys
import matplotlib.pyplot as plt
import pymysql
from PyQt5.QtWidgets import *

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='1234',
                       db='crime')

c = conn.cursor()

plt.title('plotting')
plt.plot([10, 20, 30, 40], 'r.', label='asc')
plt.plot([40, 30, 20, 10], 'g^', label='desc')
plt.legend()
plt.show()
