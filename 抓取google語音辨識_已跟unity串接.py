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
import io,codecs
cwd="C:\Python27\Scripts\ChromeWebDrive\chromedriver.exe"
driver=webdriver.Chrome(cwd)
driver.get("https://translate.google.com.tw/#zh-CN/zh-TW/")
def Sound(Line):  #發聲
    Sound_Str=io.open('C:\Sound_Str.txt', 'r',encoding = 'utf-8') #文字檔位置
    User_Sound = Sound_Str.readline() #逐行讀取文字檔
    Line=int(Line)-1
    for i in range(Line):
        User_Sound = Sound_Str.readline() #要第幾行就迴圈幾次取值
        if User_Sound=="":
            driver.quit()#關閉瀏覽器
            sys.exit() #退出程序
    driver.get("https://translate.google.com.tw/#zh-CN/zh-TW/"+User_Sound) #User_Sound是使用者對網頁Get傳輸值(文字檔內容)
    time.sleep(2)
    driver.find_element_by_css_selector("#gt-src-listen > span.jfk-button-img").click()
    time.sleep(10)
    WriteTxt("3") #發音完畢


def RunMic():
    driver.find_element_by_css_selector("#gt-speech > span.jfk-button-img").click()
    time.sleep(10)
    driver.find_element_by_css_selector("#gt-speech > span.jfk-button-img").click()
    soup = BeautifulSoup(driver.page_source,"html.parser")
    eleNum=0
    for ele in soup.select("span"):
        eleNum=eleNum+1
        ele=str(ele)
        if eleNum==48:
            ele=ele.split('''"''')[1]
            print ele
            WriteTxt(ele)
def WriteTxt(writeTxtInput):
	#f = io.open('C:\\A.txt', 'w',encoding = 'UTF-8')
	f = open('C:\\A.txt', 'w')
	f.write(writeTxtInput)
	f.truncate()
WriteTxt("3") #發音初始化
Sound_Line=1 #從第一行發音
while True:
	iNum=0
	try:
		for i in open('C:\\A.txt', 'r'):
			iNum=iNum+1
			if iNum==1:
				i=i[0:1]
			if i == "1":  #如果文字檔內的文字是1，即為辨識狀態
				print "Yes"
				RunMic()
			elif i == "2": #如果文字檔內的文字是2，就播放聲音
				if Sound_Line==7:
					Sound(Sound_Line)
					print Sound_Line
					Sound_Line=Sound_Line+1 #每隔幾行讀取文字發聲

				print Sound_Line
				Sound(Sound_Line)
				Sound_Line=Sound_Line+2 #每隔幾行讀取文字發聲

			else:
				pass
	except IOError:
		pass
	except UnboundLocalError:
		pass
	pass
