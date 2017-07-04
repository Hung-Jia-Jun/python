# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,sys
from bs4 import BeautifulSoup
import datetime
from time import *
from urllib.request import urlopen
# 导入SQLite驱动:
import sqlite3
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('Kmart.db')
# 创建一个Cursor:
cursor = conn.cursor()
# 执行一条SQL语句，创建user表:
#cursor.execute('create table user (ItemImg varchar(20),ItemName varchar(20),Price varchar(20)),ItemUrl varchar(20)')
#照片網址、   品名、     價格、  網址
#ItemImg、ItemName、Price、ItemUrl

def insertData():
    num=0
    

KeyWord="Men's Jeans"#input()
browser=webdriver.Firefox()
browser.get('http://www.kmart.com/')
browser.find_element_by_id("keyword").send_keys(KeyWord)#填入查詢關鍵字
browser.find_element_by_id("goBtn").click()

#webpage = urlopen("file:///Users/Jason/Desktop/Kmart_Crawler/Test.html").read()
soup = BeautifulSoup(browser.page_source,"html.parser")
def ItemHref():
    href_li=[]
    num=0
    for ele in soup.select("a[bo-href='product.url']"):
        if str(soup.select("a[bo-href='product.url']")[num]).find('''pricing''')>0:
            href_li.append("http://www.kmart.com"+ele["href"])
        num+=1
    return href_li

HrefLi=ItemHref() #商品list
#sleep(5)
def Crawler():
    global HrefLi
    num=0
    
    pdb.set_trace()
    PageScroll=0
    for ele in soup.select("span[class='card-price ng-binding ng-scope card-price-orig']"):
        print (soup.select("img[class='card-image']")[num]["src"]) #商品圖片
        print (soup.select("h3[class='card-title']")[num].text)#商品說明
        print (ele.text) #商品價格
        print (HrefLi[num]) #商品網址
        driver.execute_script('window.scrollTo('+str(PageScroll)+','+str(PageScroll+300)+');')
        PageScroll+=300
        num+=1
Crawler()

