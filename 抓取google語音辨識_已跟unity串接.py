# -*- coding: utf-8 -*-
import os
#os.system("pip install --upgrade pip")
#os.system("pip install bs4")
#os.system("pip install codecs")
#os.system("pip install selenium")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
import datetime, time,pdb
import io,codecs
SceneMode_Setting=""
cwd="C:\Python27\Scripts\chromedriver.exe"
driver=webdriver.Chrome(cwd)
driver.get("https://translate.google.com.tw/#zh-CN/zh-TW/")
Language_Select=""
SceneMode_Array=[]
def WriteTxt(writeTxtInput):
	f = open('C:\\A.txt', 'w')
	f.write(writeTxtInput)
	f.truncate()
def WriteSoundTxt(writeTxtInput):
	f = open('C:\\PlaySound.txt', 'w')
	f.write(writeTxtInput)
	f.truncate()
def WriteRecogTxt(writeTxtInput): #寫入給unity
	f = open('C:\\RecogContant.txt', 'w')
	f.write(writeTxtInput)
	f.truncate()
def Sound(Language_Select):  #語言選擇、發聲
	for i in open('C:\\PlaySound.txt','r'):
		User_Sound=i
		print "User_Sound:",User_Sound
	if User_Sound=="":
		pass
	driver.get("https://translate.google.com.tw/#"+Language_Select+"/"+Language_Select+"/"+User_Sound) #User_Sound是使用者對網頁Get傳輸值(文字檔內容)
	time.sleep(2)
	try:
		driver.find_element_by_css_selector("#gt-src-listen > span.jfk-button-img").click()
	except :
		pass
	WriteTxt("3") #發音完畢
	WriteSoundTxt("")
	#pdb.set_trace()

def RunMic(Elenum): #開啟麥克風
	driver.find_element_by_css_selector("#gt-speech > span.jfk-button-img").click()
	time.sleep(5)
	driver.find_element_by_id("result_box").click()
	driver.find_element_by_css_selector("#gt-speech > span.jfk-button-img").click()
	soup = BeautifulSoup(driver.page_source,"html.parser")
	eleNum=0
	#print soup
	for ele in soup.select("span"):
		eleNum=eleNum+1
		ele=str(ele)
		if (eleNum==56):
			ele=ele.split('''"''')[1]
			print ele
			if ele=="jfk-button-img":
				soup = BeautifulSoup(driver.page_source,"html.parser")
				eleNum=0
				for ele in soup.select("span"):
					eleNum=eleNum+1
					ele=str(ele)
					if (eleNum==48):
						ele=ele.split('''"''')[1]
						print ele
						WriteTxt("3") #辨識完畢
						WriteRecogTxt(ele) #寫入給辨識完畢的檔案
			else:
				WriteTxt("3") #辨識完畢
				WriteRecogTxt(ele) #寫入給辨識完畢的檔案
WriteTxt("3") #發音初始化
Sound_Line=1 #從第一行發音
temp_Langue=""
while True:
	iNum=0
	Setting_Num=0
	try:
		for setting_Langue in open('C:\\Player_Setting.txt', 'r'):
		    Setting_Num=Setting_Num+1
		    setting_Langue=str(setting_Langue)
		    if Setting_Num==3:
		        setting_Langue=repr(setting_Langue)
		        setting_Langue=setting_Langue.split("\\n")[0]
		        setting_Langue=setting_Langue.split("""'""")[1]
		        if setting_Langue=="":
		            print ""  #當未設定語言時，就等待
		        elif setting_Langue=="Language=Chinese":
		        	Language_Select="zh-CN"  #語言選擇變為中文
		            temp_Langue=setting_Langue #把目前的設定存入暫存器中
		            #print "Chinese"
		        elif setting_Langue=="Language=German":
		            Language_Select="de"  #語言選擇變為中文
		            #print "Germen"
		        elif setting_Langue=="Language=English":
		            Language_Select="en"  #語言選擇變為中文
			if temp_Langue!=Language_Select:
				driver.get("https://translate.google.com.tw/#"+Language_Select+"/"+Language_Select+"/") #更換辨識語言
	        	temp_Langue=setting_Langue
			for i in open('C:\\A.txt', 'r'):
					iNum=iNum+1
					if iNum==1:
						Sound_Mode=i[0:1] #偵測是否於發音模式
					if Sound_Mode == "1":  #如果文字檔內的文字是1，即為辨識狀態
						print u"開啟麥克風"
						RunMic(56)
					elif Sound_Mode == "2": #如果文字檔內的文字是2，就播放聲音
						print u"播放聲音"
						Sound(Language_Select)
					elif Sound_Mode=="4": #當unity 發送一個退出的訊號
						driver.quit()#關閉瀏覽器
						sys.exit() #退出程序
					else:
						pass
	except IOError:
		pass
	except UnboundLocalError:
		pass
	pass

