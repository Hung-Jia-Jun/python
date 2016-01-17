# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
#指定使用Firefox瀏覽器
browser=webdriver.Firefox()
#進入英雄聯盟戰績網的index
browser.get('http://lol.moa.tw/summoner/index')
key = raw_input("Please set Player ID=").decode(sys.stdin.encoding)
browser.find_element_by_id("searchlogsSn").send_keys(key)

browser.find_element_by_id("querySubmit").click()
browser.find_element_by_link_text(u"近期對戰").click()
time.sleep(5)
for i in range (1,0,-1):
    browser.find_element_by_id("summoner_more").click()
   

soup = BeautifulSoup(browser.page_source,"html.parser")

for ele in soup.select('.success'):
	for ele2 in soup.select('.strong'):
		print ele2.text
		print ele.text
	
browser.close()
