# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
import datetime, time
browser=webdriver.Firefox()
browser.get('http://w.wantgoo.com/')
print u"請輸入股票名or股票代號"
key = raw_input("").decode(sys.stdin.encoding)
browser.find_element_by_id("txtSearchStock").send_keys(key)
time.sleep(2)
browser.find_element_by_id("btnHeaderSearch").click()

browser.find_element_by_id("BoolingerD").click()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
file_name = "ScreenShot" + st + ".png"
time.sleep(5)
browser.save_screenshot(file_name)

browser.get('https://www.facebook.com/')

    
browser.find_element_by_id("._552m").send_keys(key)



    
