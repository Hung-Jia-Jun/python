# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
import getpass
#指定使用Firefox瀏覽器
student_browser=webdriver.Firefox()
print u"--------------------------------------------------------------------------------------"
print u"歡迎使用台北海洋技術學院自動請假系統，這是由一個每天睡到自然醒的學長寫的"
print u"只要把這個腳本掛到開機啟動資料夾內"
print u"一起床開電腦後"
print u"就會幫你找找看哪個老師又記你曠課了，這時此程式就會自動執行"
print u"然後....你就可以繼續去睡覺or玩遊戲惹"
print u"現在～"
print u"--------------------------------------------------------------------------------------"
print u"請輸入學生資訊網登入帳號:"
account_key = raw_input().decode(sys.stdin.encoding)
print u"--------------------------------------------------------------------------------------"
print u"請輸入學生資訊網密碼:"
password_key = getpass.getpass("").decode(sys.stdin.encoding)
print u"--------------------------------------------------------------------------------------"
try:
	student_browser.get('http://140.129.253.29/personal/pstudent/login.aspx')
	student_browser.find_element_by_name("sID").send_keys(account_key)
	student_browser.find_element_by_name("sPassword").send_keys(password_key)
	student_browser.find_element_by_name("btnOk").click()
	student_browser.find_element_by_link_text(u"請假缺曠查詢").click()
	soup = BeautifulSoup(student_browser.page_source,"html.parser")
	studentNUM=0
except :
	print u'帳號或密碼輸入錯誤'
	pass
for ele in soup.select('tr'):
	studentNUM=studentNUM+1
	if studentNUM==2:
		print u"您可以請假的最近兩節課是:"
		Daystr=ele.select('td')[2].text
		Daysplit=Daystr.split('/')[2]
		Lessonstr=ele.select('td')[4].text
		print ele.select('td')[1].text,ele.select('td')[2].text,ele.select('td')[4].text
	if studentNUM==3:
		Daystr2=ele.select('td')[2].text
		Daysplit2=Daystr2.split('/')[2]
		Lessonstr2=ele.select('td')[4].text
		print ele.select('td')[1].text,ele.select('td')[2].text,ele.select('td')[4].text



student_browser.get('http://140.129.253.29/Usc/HomePage/flogin.aspx')
student_browser.find_element_by_name("txtAccount").send_keys(account_key)
student_browser.find_element_by_name("txtPwd").send_keys(password_key)
student_browser.find_element_by_css_selector("input[type=\"submit\"]").click()
student_browser.get('http://140.129.253.29/Usc/Std/Usc_Std_ApplyCase.aspx')
Select(student_browser.find_element_by_name("ApplyUnit")).select_by_visible_text(u"生輔組")
Select(student_browser.find_element_by_name("ApplyItem")).select_by_visible_text(u"學生請假單")
student_browser.find_element_by_name("add").click()



Daytostr=raw_input().decode(sys.stdin.encoding)
Daytostr2=raw_input().decode(sys.stdin.encoding)
Lessontostr=raw_input().decode(sys.stdin.encoding)
Lessontostr2=raw_input().decode(sys.stdin.encoding)
student_browser.switch_to_window(student_browser.window_handles[-1])
Select(student_browser.find_element_by_name("S_Day")).select_by_visible_text(Daytostr)
Select(student_browser.find_element_by_name("E_Day")).select_by_visible_text(Daytostr2)
Select(student_browser.find_element_by_name("S_Section")).select_by_visible_text(Lessontostr)
Select(student_browser.find_element_by_name("E_Section")).select_by_visible_text(Lessontostr2)
Select(student_browser.find_element_by_name("Hcode")).select_by_visible_text(u"病假")
print u"輸入你不小心生病的理由:"
Reasoninput = raw_input().decode(sys.stdin.encoding)
student_browser.find_element_by_name("Reason").send_keys(Reasoninput)
student_browser.find_element_by_css_selector("input[type=\"button\"]").click()
