# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
browser=webdriver.Firefox()
browser.get('http://lol.moa.tw/summoner/index')
key = raw_input("Please set Player ID=").decode(sys.stdin.encoding)
browser.find_element_by_id("searchlogsSn").send_keys(key)

browser.find_element_by_id("querySubmit").click()
browser.find_element_by_link_text(u"近期對戰").click()
time.sleep(5)
for i in range (20,0,-1):
    browser.find_element_by_id("summoner_more").click()
soup = BeautifulSoup(browser.page_source,"html.parser")
try :
    for ele in soup.select('th'):
        
         print ele.text

except:
       pass


    




    
