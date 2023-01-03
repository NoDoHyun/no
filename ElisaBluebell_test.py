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

plt.plot([1, 2, 3, 4], [12, 43, 25, 15])
plt.show()