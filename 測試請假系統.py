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
#進入學生資訊網的index
print u"請輸入登入帳號:"
account_key = raw_input().decode(sys.stdin.encoding)
print u"請輸入學生資訊網密碼:"
password_key = getpass.getpass("").decode(sys.stdin.encoding)


student_browser.get('http://140.129.253.29/Usc/HomePage/flogin.aspx')
student_browser.find_element_by_name("txtAccount").send_keys(account_key)
student_browser.find_element_by_name("txtPwd").send_keys(password_key)
student_browser.find_element_by_css_selector("input[type=\"submit\"]").click()
student_browser.get('http://140.129.253.29/Usc/Std/Usc_Std_ApplyCase.aspx')  #案件申請網頁
Select(student_browser.find_element_by_name("ApplyUnit")).select_by_visible_text(u"生輔組")
Select(student_browser.find_element_by_name("ApplyItem")).select_by_visible_text(u"學生請假單")
student_browser.find_element_by_name("add").click()



student_browser.switch_to_window(student_browser.window_handles[-1])
Select(student_browser.find_element_by_name("S_Day")).select_by_visible_text("5")
Select(student_browser.find_element_by_name("E_Day")).select_by_visible_text("5")
Select(student_browser.find_element_by_name("S_Section")).select_by_visible_text("07")
Select(student_browser.find_element_by_name("E_Section")).select_by_visible_text("08")
Select(student_browser.find_element_by_name("Hcode")).select_by_visible_text(u"病假")
print u"輸入你不小心生病的理由:"
Reasoninput = raw_input().decode(sys.stdin.encoding)
student_browser.find_element_by_name("Reason").send_keys(Reasoninput)
student_browser.find_element_by_css_selector("input[type=\"button\"]").click()
