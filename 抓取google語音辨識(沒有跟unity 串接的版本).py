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
cwd="C:\Python27\Scripts\ChromeDriver\chromedriver.exe"
browser=webdriver.Chrome(cwd)

def RunMic():
	browser.find_element_by_id("start_button").click()
	time.sleep(10)
	browser.find_element_by_id("start_button").click()
	for ele in soup.select('.results'):
		print ele.text
		writeTxtInput=ele.text
	WriteTxt(writeTxtInput)
def startBroswer():
	browser.get('https://www.google.com/intl/en/chrome/demos/speech.html')

	Select(browser.find_element_by_id("select_language")).select_by_value("36")
	Select(browser.find_element_by_id("select_dialect")).select_by_value("cmn-Hant-TW")

def WriteTxt(writeTxtInput):
	f = io.open('C:\A.txt', 'w',encoding = 'UTF-8')
	f.write(writeTxtInput)
	time.sleep(5)
	f.truncate()
def TXTControl():
	iNum=0
	try:
		for i in open('C:\A.txt', 'r'):
			iNum=iNum+1
			if iNum==1:
				i=i[0:1]
		if i == "1":  #如果文字檔內的文字是1，即為辨識狀態
			RunMic()
		else:
			pass
	except IOError:
		pass
	except UnboundLocalError:
		pass
startBroswer()		
while True:
	TXTControl()
	pass

