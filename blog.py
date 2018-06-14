# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import jieba.analyse
import MySQLdb
from Tkinter import *
import ttk
import os
titles=set()
d=[]
#header={}
dict={}
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
def parse_title(urls):
        html=download(urls)
        if html is None:
            return None
        parse_descrtion(html)
        soup=BeautifulSoup(html,"html.parser")
        links=soup.find_all('h4',attrs={'class':'text-truncate'})
        for link in links:
            titles.add(link.get_text())

def download(url):
    if url is None:
        return None
    try:
        response=requests.get(url,headers=header)
        if (response.status_code == 200):
        #response.raise_for_status()
            return response.content
    except:
        return None
    
#解析摘要
def parse_descrtion(html):
    if html is None:
        return None
    soup=BeautifulSoup(html,"html.parser")
    discriptions=soup.find_all('p',attrs={'class':'content'})
    for link in discriptions:
        titles.add(link.get_text())

def jiebaSet():
    strs=''
    if titles.__len__()==0:
        return
    for item in titles:
        strs=strs+item;

    tags = jieba.analyse.extract_tags(strs, topK=50, withWeight=True)
    p=re.compile(r"[a-zA-Z]")
    for items in tags:
        if re.findall(p,items[0]):
            key=items[0].lower()
            if key in dict:
                dict[key]+=items[1]
            else:
                dict[key]=items[1]
        else:
            key=items[0]
            dict[key]=items[1]

    z = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    for key ,value in z[1:]:
        keynames=key
        #l2=(dict.values()*1000)
        countes=int(value*1000)
        cursor.execute("insert into h3(keyname,counte) values ('%s','%d')"%(keynames,countes))
        db.commit()
        #print keynames,counte
        #print(item[0] + '\t '+ str(int(item[1] * 1000)))
        #print item[0],(item[1]*1000)

def web():
    win=Tk()
    win.geometry('700x500+500+300')
    win.title("spider GUI")
    l1 = Label(win,text = '请输入网址:')
    l1.grid(row=0,column=0)
    l2 = Label(win,text = '请输入消息头:')
    l2.grid(row=1,column=0)
    v1=StringVar()
    v2=StringVar()
    e1=Entry(win,textvariable=v1)
    e1.grid(row=0,column=1,padx=10,pady=10)
    comboxlist=ttk.Combobox(win,textvariable=v2)
    comboxlist["values"]=('User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50','User-Agent:Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50')


    comboxlist.grid (row=1,column=1,padx=20,pady=10)
    comboxlist.current(0)
    def geturl():
        print "Start Crawling,please wait........ "
        global url
        #global getuseagent
        url=e1.get()
        #header=comboxlist.get()
        win.destroy()
        for i in range(1,8):
            fulurl=url+"/forezp/article/list/"+str(i)
            #win.destroy()
            html = parse_title(fulurl)
            #download(html)
            #parse_descrtion(html)
        #win.destroy()
    def getuseagent():
        win.destroy()
    button1 = Button(win,text=u'确定',command=geturl)
    button1.grid(row=2, column=0)
    button2 = Button(win,text=u'退出',command=getuseagent)
    button2.grid(row=2, column=2)
    win.mainloop()   

if __name__=='__main__':
    #url = "https://blog.csdn.net"
    #html=parse_title(url)
    #parse_descrtion(html)
    fulurl=''
    web()
    db = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='hiphop', charset='utf8')
    cursor = db.cursor()
    cursor.execute('drop table if exists h3')
    tables='''
        create table h3(
          id int auto_increment primary key not null,
          keyname varchar(30) not null,
          counte int not null
        )
        '''
    cursor.execute(tables)
    jiebaSet()
    db.close()
    os.system("python E:\spiders\mysql.py")
    #os.system("python E:\spiders\paixu.py")




