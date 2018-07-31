# -*- coding:utf-8 -*-
import requests
import urllib,urllib2
import cookielib
from json import loads
import re
c=cookielib.LWPCookieJar()
cookie=urllib2.HTTPCookieProcessor()
opener=urllib2.build_opener(cookie)
urllib2.install_opener(opener)
from config import station_names
from time import sleep
dict={}
for i in station_names.split('@')[1:]:
    stationlist=i.split('|')
    dict[stationlist[1]]=stationlist[2]

train_date='2018-05-24'
fromstation='成都'
from_station=dict[fromstation]
tostation='长沙'
to_station=dict[tostation]
#captcha_url="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9585229891654816"
headers=headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
def login():
    print "正在获取验证码"
    req=urllib2.Request("https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9585229891654816")
    req.headers=headers
    imagecode=opener.open(req).read()
    with open("code.png","wb") as fn:
        fn.write(imagecode)
    print "正在识别验证码"
    req=urllib2.Request("https://kyfw.12306.cn/passport/captcha/captcha-check")
    req.headers=headers
    code=raw_input("请输入验证码：")
    data={
        'answer': code,
        'login_site': 'E',
        'rand': 'sjrand'
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data).read()
    req=urllib2.Request("https://kyfw.12306.cn/passport/web/login")
    req.headers=headers
    #usename=raw_input("请输入用户名：")
    #passwd=raw_input("请输入密码：")
    data={
        'username': 'aaaaa',
        'password':'aaaaa',
        'appid': 'otn'

    }
    data=urllib.urlencode(data)
    html=opener.open(req,data).read()
    result=loads(html)
    if  result['result_code']==0:
        print "登录成功"
        req=urllib2.Request("https://kyfw.12306.cn/otn/login/userLogin")
        req.headers=headers
        data={
            '_json_att':''
        }
        data=urllib.urlencode(data)
        html=opener.open(req,data=data)
        req=urllib2.Request("https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin")
        req.headers=headers
        html=opener.open(req)
        #print html.geturl()
        req=urllib2.Request("https://kyfw.12306.cn/passport/web/auth/uamtk")
        req.headers=headers
        data={
            'appid':'otn'
        }
        data=urllib.urlencode(data)
        html=opener.open(req,data=data).read()
       # print html
        result=loads(html)
        tk=result['newapptk']
        req=urllib2.Request("https://kyfw.12306.cn/otn/uamauthclient")
        req.headers=headers
        data={
            'tk':tk

        }
        data=urllib.urlencode(data)
        html=opener.open(req,data=data)
        print html
        req=urllib2.Request("https://kyfw.12306.cn/otn/index/initMy12306")
        req.headers=headers
        html=opener.open(req).read()
        #print html
        return True
    print "登录失败，正在重新登录："
    sleep(5)

    login()
login()
def chek_tiket():
    req=urllib2.Request("https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" %(train_date,from_station,to_station))
    #req=urllib2.Request("https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-13&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=AOH&purpose_codes=ADULT")
    req.headers=headers
    html=opener.open(req).read()
    #print html
    result=loads(html)
    data=result['data']['result']
    return data
'''
[3]车次
[8]出发时间
[9]到达时间
[10]历时
[31]一等座
[33]动卧
[26]无座
[22]其他
[23]软卧
[28]硬卧
[2]train_no
[12]leftTicket
[4][6]fromStationTelecode
[3]stationTrainCode
[15]train_location
[13]出发日期
'''

for i in chek_tiket():
    templist=i.split("|")

    try:
        if templist[28]==u"有"or int(templist[28])>0:
            print u'''
            该车次有票:
            车次：%s
            出发时间：%s
            到达时间：%s
            历时：%s
            硬卧余票：%s
            '''%(templist[3],templist[8],templist[9],templist[10],templist[28])
            break
    except:
        continue


def buytiket():
    req=urllib2.Request("https://kyfw.12306.cn/otn/index/initMy12306")
    req.headers=headers
    html=opener.open(req).read()
    #第一个请求
    req=urllib2.Request("https://kyfw.12306.cn/otn/login/checkUser")
    req.headers=headers
    data={
       '_json_att':''
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    #print 100001,html
    req=urllib2.Request("https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest")
    req.headers=headers
    data={
        'secretStr': urllib.unquote(templist[0]),
        'train_date': train_date,
        'back_train_date': '2018 - 05 - 24',
        'tour_flag':'dc',
        'purpose_codes': 'ADULT',
        'query_from_station_name': fromstation,
        'query_to_station_name': tostation,
        'undefined':'',
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    #print 1002,html
    #第三个请求
    req=urllib2.Request("https://kyfw.12306.cn/otn/confirmPassenger/initDc")
    req.headers=headers
    data={
       '_json_att':''
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    #print html
    globalRepeatSubmitToken=re.findall(r"globalRepeatSubmitToken = '(.*?)'",html)
    key_check_isChange=re.findall(r"'key_check_isChange':'(.*?)'",html)
    print 10003,globalRepeatSubmitToken,key_check_isChange
    #第四个请求
    req=urllib2.Request("https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs")
    req.headers=headers
    data={
    '_json_att':'',
    'REPEAT_SUBMIT_TOKEN':globalRepeatSubmitToken
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    print 10004,html
    req=urllib2.Request("https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo")
    req.headers=headers
    data={
        '_json_att':'',
        'bed_level_order_num':'000000000000000000000000000000',
        'cancel_flag':'2',
        'oldPassengerStr':'罗立民,1,433122199307254513,3_',
        'passengerTicketStr':'3,0,1,罗立民,1,433122199307254513,17761263649,N',
        'randCode':'',
        'REPEAT_SUBMIT_TOKEN':globalRepeatSubmitToken,
        'tour_flag':'dc',
        'whatsSelect':'1',
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    print 1005,html
    req=urllib2.Request("https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount")
    req.headers=headers
    data={
        '_json_att':'',
        'fromStationTelecode':templist[4],
        'leftTicket':templist[12],
        'purpose_codes':'00',
        'REPEAT_SUBMIT_TOKEN':globalRepeatSubmitToken,
        'seatType':'3',
        'stationTrainCode':templist[3],
        'toStationTelecode':to_station,
        'train_date':'Thu+May+24+2018+00:00:00+GMT+0800',
        'train_location':templist[15],
        'train_no':templist[2],
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    print 1006,html
    req=urllib2.Request("https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue")
    req.headers=headers
    data={
        '_json_att':'',
        'choose_seats':'',
        'dwAll':'N',
        'key_check_isChange':key_check_isChange,
        'leftTicketStr':templist[12],
        'oldPassengerStr':'罗立民,1,433122199307254513,3_',
        'passengerTicketStr':'3,0,1,罗立民,1,433122199307254513,17761263649,N',
        'purpose_codes':'00',
        'randCode':'',
        'REPEAT_SUBMIT_TOKEN':globalRepeatSubmitToken,
        'roomType':'00',
        'seatDetailType':'000',
        'train_location':templist[15],
        'whatsSelect':'1',
 }
    data=urllib.urlencode(data)
    html=opener.open(req,data)
    print html.geturl()
buytiket()
