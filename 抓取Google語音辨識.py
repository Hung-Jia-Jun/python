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
import io
def WriteTxt(writeTxtInput):
	f = io.open('D:\Speech recognition5.3\Assets\A.txt', 'w',encoding = 'UTF-8')
	f.write(writeTxtInput)
	time.sleep(5)
	f.truncate()
cwd="C:\Python27\Scripts\WebDrive\chromedriver.exe"
browser=webdriver.Chrome(cwd)
browser.get('https://www.google.com/intl/en/chrome/demos/speech.html')


Select(browser.find_element_by_id("select_language")).select_by_value("36")
Select(browser.find_element_by_id("select_dialect")).select_by_value("cmn-Hant-TW")
browser.find_element_by_id("start_button").click()
time.sleep(10)

browser.find_element_by_id("start_button").click()
soup = BeautifulSoup(browser.page_source,"html.parser")
for ele in soup.select('.interim'):
	print ele.text
	writeTxtInput=ele.text
WriteTxt(writeTxtInput)
for i in io.open('D:\Speech recognition5.3\Assets\A.txt', 'r',encoding = 'UTF-8'):
  print i
