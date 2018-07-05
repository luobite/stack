# -*- coding:utf-8 -*-
import MySQLdb
import matplotlib.pyplot as plt
from pylab import *
import pyttsx
import win32com.client
mpl.rcParams['font.sans-serif'] = ['SimHei']
if __name__=='__main__':
    db = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='hiphop', charset='utf8')
    cursor = db.cursor()
    cursor.execute("select keyname,counte from h3")
    rows=cursor.fetchall()
    list1=[]
    list2=[]
    for row in rows:
        list1.append(row[0])
        list2.append(row[1])
    plt.bar(list1[:5],list2[:5],label=u"关键词")
    plt.legend()
    plt.xlabel(u'关键字')
    plt.ylabel(u'权重值')
    plt.title(u'关键字展示图')
    plt.show()
    labels=list1[:5]
    sizes=list2[:5  ]
    #explode = (0.1, 0, 0, 0)
    plt.pie(sizes,  labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    plt.show()
    #engine = pyttsx.init()
    #rate = engine.getProperty('rate')
    #engine.setProperty('rate', rate - 50)
    #engine.say('Top two key worlds are Openresty springcloud ')
    #engine.runAndWait()
    #engine.endLoop()

