# -*- coding:utf-8 -*-
from selenium import webdriver
import time
d=webdriver.PhantomJS()
d.get("https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=")
time.sleep(3)
d.save_screenshot("douban.png")
js = "document.body.scrollTop=10000"
d.execute_script(js)
time.sleep(5)
d.save_screenshot("newdouban.png")
d.quit()