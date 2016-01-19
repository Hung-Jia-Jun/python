#coding=utf-8
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
def selection_Day_lesson(Daystr,Daystr2,Lessonstr,Lessonstr2):
	student_browser.switch_to_window(student_browser.window_handles[-1])
	Select(student_browser.find_element_by_name("S_Day")).select_by_value(Daystr)
	Select(student_browser.find_element_by_name("E_Day")).select_by_visible_text(Daystr2)
	Select(student_browser.find_element_by_name("S_Section")).select_by_visible_text(Lessonstr)
	Select(student_browser.find_element_by_name("E_Section")).select_by_visible_text(Lessonstr2)
	Select(student_browser.find_element_by_name("Hcode")).select_by_visible_text(u"病假")
	print u"輸入你不小心生病的理由:"
	Reasoninput = raw_input().decode(sys.stdin.encoding)
	student_browser.find_element_by_name("Reason").send_keys(Reasoninput)
	student_browser.find_element_by_css_selector("input[type=\"button\"]").click()
	print u"請假完畢"
	#student_browser.quit()
	return 0






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
	print u"正在登入學生資訊網......"
	student_browser.get('http://140.129.253.29/personal/pstudent/login.aspx')
	student_browser.find_element_by_name("sID").send_keys(account_key)
	student_browser.find_element_by_name("sPassword").send_keys(password_key)
	student_browser.find_element_by_name("btnOk").click()
except :
	print u'帳號或密碼輸入錯誤'
	pass
print u"登入成功"
print u"正在查詢請假缺曠資訊......"
try:
	student_browser.find_element_by_link_text(u"請假缺曠查詢").click()
	soup = BeautifulSoup(student_browser.page_source,"html.parser")
except:
	for i in range(5, 0, -1):
		student_browser.find_element_by_link_text(u"請假缺曠查詢").click()
		soup = BeautifulSoup(student_browser.page_source,"html.parser")




print u"查詢完畢"


studentNUM=0
for ele in soup.select('tr'):
	studentNUM=studentNUM+1
	if studentNUM==2:
		print u"--------------------------------------------------------------------------------------"
		print u"您可以請假的最近兩節課是:"
		Daystr=ele.select('td')[2].text
		Daysplit=Daystr.split("/")[2]
		Daystrip=Daysplit[0:1]
		Lessonstr=ele.select('td')[4].text
		Lessonstrstrip=Lessonstr[0:2]
		print ele.select('td')[1].text,ele.select('td')[2].text,ele.select('td')[4].text
	if studentNUM==3:
		Daystr2=ele.select('td')[2].text
		Daysplit2=Daystr.split('/')[2]
		Daystrip2=Daysplit2[0:1]
		Lessonstr2=ele.select('td')[4].text
		Lessonstrstrip2=Lessonstr2[0:2]
		print ele.select('td')[1].text,ele.select('td')[2].text,ele.select('td')[4].text
		print u"--------------------------------------------------------------------------------------"


print u"正在登入聯合服務中心......"
student_browser.get('http://140.129.253.29/Usc/HomePage/flogin.aspx')
student_browser.find_element_by_name("txtAccount").send_keys(account_key)
student_browser.find_element_by_name("txtPwd").send_keys(password_key)
student_browser.find_element_by_css_selector("input[type=\"submit\"]").click()

student_browser.get('http://140.129.253.29/Usc/Std/Usc_Std_ApplyCase.aspx')
print u"開啟學生請假單填入資料中......"
Select(student_browser.find_element_by_name("ApplyUnit")).select_by_visible_text(u"生輔組")
Select(student_browser.find_element_by_name("ApplyItem")).select_by_visible_text(u"學生請假單")
student_browser.find_element_by_name("add").click()

selection_Day_lesson(Daystrip,Daystrip2,Lessonstrstrip,Lessonstrstrip2)
student_browser.quit()

#這邊是未測試成功的區塊
"""
print u"正在查詢請假是否成功......"
student_browser.get('http://140.129.253.29/Usc/HomePage/flogin.aspx')
student_browser.find_element_by_name("txtAccount").send_keys(account_key)
student_browser.find_element_by_name("txtPwd").send_keys(password_key)
student_browser.find_element_by_css_selector("input[type=\"submit\"]").click()


student_browser.get('http://140.129.253.29/Usc/Std/Usc_Std_ApplyCase.aspx')
print u"進入查詢頁面中......"
Select(student_browser.find_element_by_name("ApplyUnit")).select_by_visible_text(u"生輔組")
Select(student_browser.find_element_by_name("ApplyItem")).select_by_visible_text(u"學生請假單")
student_browser.find_element_by_name("query").click()


studentquery=0
for ele in soup.select('tr'):
	ele.select('td').text
"""
