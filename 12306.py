# -*- coding:utf-8 -*-
import requests
from json import loads
s=requests.session()
captcha_check="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
res=s.get(captcha_check,headers=headers)

with open("captcha.png","wb") as f:
    f.write(res.content)
url="https://kyfw.12306.cn/passport/captcha/captcha-check"
data=raw_input("请输入验证码：")
form_data={
    'answer': data.split( ),
    'login_site': 'E',
    'rand': 'sjrand'
}
response=s.post(url,headers=headers,data=form_data)
#print response.content
dict=loads(response.content)
code=dict['result_code']
if str(code)=='4':
    print "验证码校验成功"
else:
    print "验证码校验失败"
#登录
loginurl="https://kyfw.12306.cn/passport/web/login"
logdata={
    'username': 'llm164826761',
    'password': 'qw164826761',
    'appid': 'otn'
}
ress=s.post(loginurl,headers=headers,data=logdata)
dic=loads(ress.content)
mes=dic['result_message']
if mes==u"登录成功":
    print "登录成功"
else:
    print "登录失败"
geturl="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-24&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=SHH&purpose_codes=ADULT"
tiket=s.get(geturl,headers=headers)
dics=loads(tiket.content)
print dics