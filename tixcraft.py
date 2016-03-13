#coding=utf-8
import requests
import urllib2,pdb
from bs4 import BeautifulSoup 
import string,sys,re,io,os
from requests import Request, Session
from  urllib  import  quote 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
isbreak=0
ReturnUrl_intNum=0
UrlArray=[]
findList=[]
tmpList=0
print u"請輸入購票網址:"
TicketUrl=raw_input().decode(sys.stdin.encoding)
TicketUrl2=TicketUrl.replace("detail","game")

print u"請輸入指定票種:"
userfindWord1=raw_input().decode(sys.stdin.encoding)
print u"請輸入購買張數"
ticketNum=raw_input().decode(sys.stdin.encoding)
def  OnlyCharNum(s,oth = ''):#用這個函式可以將特殊字元去除掉，只顯示fomart這個字串列中的數值
    s2  =  s.lower();
    fomart  =  'abcdefghijklmnopqrstuvwxyz0123456789_"/'
    for  c  in  s2:
        if  not  c  in  fomart:
            s  =  s.replace(c,'');
    return  s;
def magic(numList):         # [1,2,3]
    s3 = map(str, numList)   # ['1','2','3']
    s3 = ''.join(s3)          # '123'
    s3 = int(s3)              # 123
    return s3
def AllTicket ():
    elenum=0
    ticketText=-1
    for ele in soup.select("li"):
        elenum=elenum+1
        ticketText=ticketText+1
        if elenum>9:
            eleencode=ele.text
            eleencode2=eleencode.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
            print eleencode2.replace("?","*")#替換"?"成"*"
def UrlGet():
    elenum=0
    for ele in soup.select("script"):
        eleurl=ele.text
    eleurl2=eleurl.split("{")[8]
    eleurl3=eleurl2
    eleurl3=eleurl2.split(":")


    try:
        tickettotal=0
        elenumlist=0
        for i in range(100,0,-1):
            tickettotal=tickettotal+1
            elenumlist=elenumlist+1
            eleurl4=eleurl3[elenumlist]
            eleurl5=OnlyCharNum(eleurl4)
            eleurl6=eleurl5.split('''"''')[1]
            url="https://tixcraft.com"+eleurl6
            UrlArray.append(url)
    except:#如果到達字元的最尾端，會產生錯誤，利用錯誤就可以跳出這個迴圈了

        pass


def CanBuyTicket():
    elenum=0
    elenum2=0
    ticketText=-1
    ArrayLen=0
    
    for ele in soup.select("li"):
        elenum=elenum+1
        ticketText=ticketText+1

        if elenum>9:
            find_ele=ele.text
            find_ele.find(findWord)
            if find_ele.find(findWord)<0:#找尋是否有"已賣完"的關鍵字，有的話就顯示在可購買的列表中
                elenum2=elenum2+1
                eleencode=ele.text
                eleencode2=eleencode.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)#將ASCII中不認識的字元替換成"?"
                print elenum2,eleencode2.replace("?","*")#為了美觀將"?"替換成"*"
                eleTicket=eleencode2.replace("?","*")#將替換後的值存給eleTicket
                ArrayLen=ArrayLen+1
                if eleTicket.find(userfindWord1) >0:
                    ReturnUrl_intNum=ArrayLen-1    #如果發現使用者輸入的關鍵字就將目前陣列位置回傳出
                    findList.append([ReturnUrl_intNum])#在陣列中追加找到的位置，以便打開網頁
def EndUrl():#剖析使用者輸入的網頁內是否有"立即購票"連結
    elenumSelect1=0
    s1=requests.Session()
    res=s1.get(TicketUrl2)
    soup1 = BeautifulSoup(res.text,"html.parser")
    for ele in soup1.select("input"):
        elenumSelect1=elenumSelect1+1
        if elenumSelect1==3:
            elehref=str(ele)#
    try:
        elehref=elehref[18:100]
        elehref=elehref.split('''"''')[0]
        eleEndUrl="https://tixcraft.com"+elehref
        return str(eleEndUrl)
    except :
       print u"未開放購票"
       EndUrl() 
       pass    
    
    pass
EndUrl()
eleEndUrl=EndUrl()
print eleEndUrl
s4=requests.Session()
res=s4.get(eleEndUrl)
soup = BeautifulSoup(res.text,"html.parser")
findWord="已售完"
findWord=findWord.decode("utf-8")


browser=webdriver.Firefox()
browser.get("https://tixcraft.com/login")
print u"請先登入"
raw_input().decode(sys.stdin.encoding)
print u"所有票種狀態:"
print AllTicket() 
print u"可以買的票種:"
CanBuyTicket()
UrlGet()
gotoUrlnum=findList[0]#將取得的list陣列存入變數以便轉換為int
gotoUrlnum=magic(gotoUrlnum)#轉換list變成int


gotoUrl=UrlArray[gotoUrlnum]
s2=requests.Session()
res=s2.get(gotoUrl)
soup2 = BeautifulSoup(res.text,"html.parser")

for ele in soup2.select("select"):#剖析網頁中"確認購買"的按鈕ID
    eletostr=str(ele)
    eletostr2=eletostr.split("=")[1] 
    eletostr3=eletostr2.split('''"''')[1]
    eletostr4=str(eletostr3)#將結果存給eletostr4供後續點擊之用


def TicketNeedNum(ticketNum):
    select.select_by_visible_text(ticketNum)
    pass

browser.get(gotoUrl)
select = Select(browser.find_element_by_id(eletostr4))
try:
    TicketNeedNum(ticketNum)
    pass
except :
    print u"請輸入正確的購票張數"
    ticketNum2=raw_input().decode(sys.stdin.encoding)
    TicketNeedNum(ticketNum2)
    pass
browser.find_element_by_id("ticketPriceSubmit").click()
