#-*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys,io


cwd="C:\Python27\Scripts\ChromeWebDrive\chromedriver.exe"
driver=webdriver.Chrome(cwd)


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
    driver.find_element_by_css_selector("#gt-src-listen > span.jfk-button-img").click()






Sound_List=3 #發聲音的第一行位置
Sound(Sound_List)
for i in range (100):
    Sound_List=Sound_List+2 #每隔幾行讀取文字發聲
    print "Pause"
    raw_input()
    Sound(Sound_List)
