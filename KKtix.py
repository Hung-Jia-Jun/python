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
import os
import unittest, time, re,sys
import  getpass 

browser=webdriver.Firefox()
browser.get("https://kktix.com/users/sign_in?back_to=http%3A%2F%2Fkktix.com%2F")
print u"請輸入你的帳號:"
Account = raw_input().decode(sys.stdin.encoding)
print u"請輸入你的密碼:"
Password = getpass.getpass("") 
print u"要執行幾次??"
settime = raw_input().decode(sys.stdin.encoding)
intsettime=int(settime)
print u"請輸入需移動到的訂票頁面:"
Url=raw_input().decode(sys.stdin.encoding)
browser.find_element_by_id("user_login").send_keys(Account)
browser.find_element_by_id("user_password").send_keys(Password)
browser.find_element_by_name("commit").click()
def openUrl():
	Enter=False
	browser.get(Url)
	time.sleep(2)
	try:
		browser.find_element_by_id("person_agree_terms").click()
		
	except :
		while Enter==False:
			browser.get(Url)
			try:
				browser.find_element_by_id("person_agree_terms").click()
			except :
				Enter=False
			else:
				Enter=True
				pass
		
			
	else :
		Enter=True
		pass
	try:
		browser.find_element_by_css_selector("label.checkbox-inline.ng-binding").click()
		browser.find_element_by_css_selector("button.btn-default.plus").click()
		browser.find_element_by_css_selector("button.btn-default.plus").click()
		browser.find_element_by_css_selector("button.btn-default.plus").click()
		browser.find_element_by_css_selector("button.btn-default.plus").click()
		try:
			browser.find_element_by_xpath("//div[@id='registrationsNewApp']/div/div[5]/div[5]/button").click()
		except :
			browser.find_element_by_xpath("//div[@id='registrationsNewApp']/div/div[5]/div[4]/button").click()
			pass
	except :
		print u"發現驗證碼"
		print u"請更換IP位置後"
		print u"請按任意鍵退出"
		raw_input().decode(sys.stdin.encoding)
		

	pass

for i in range(intsettime, 0, -1):
	openUrl()
	print u"輸入完資料後請按Enter鍵下一步"
	raw_input().decode(sys.stdin.encoding)
	
