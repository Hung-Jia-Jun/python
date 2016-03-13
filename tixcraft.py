#coding=utf-8
import requests
import urllib2,pdb
from bs4 import BeautifulSoup 
import string,sys,re,io,os,chardet
from requests import Request, Session
from  urllib  import  quote 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


UrlArray=[]
print u"請輸入購票網址:"
TicketUrl=raw_input().decode(sys.stdin.encoding)
TicketUrl2=TicketUrl.replace("detail","game")
def  OnlyCharNum(s,oth = ''):
    s2  =  s.lower();
    fomart  =  'abcdefghijklmnopqrstuvwxyz0123456789_"/'
    for  c  in  s2:
        if  not  c  in  fomart:
            s  =  s.replace(c,'');
    return  s;
def AllTicket ():
    elenum=0
    ticketText=-1
    for ele in soup.select("li"):
        elenum=elenum+1
        ticketText=ticketText+1
        if elenum>9:
            #print ele.text
            eleencode=ele.text
            eleencode2=eleencode.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
            print eleencode2.replace("?","*")
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
            
    except:

        pass


def CanBuyTicket():
    elenum=0
    elenum2=0
    ticketText=-1
    for ele in soup.select("li"):
        elenum=elenum+1
        ticketText=ticketText+1

        if elenum>9:
            find_ele=ele.text
            find_ele.find(findWord)
            if find_ele.find(findWord)<0:
                elenum2=elenum2+1
                eleencode=ele.text
                eleencode2=eleencode.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
                print elenum2,eleencode2.replace("?","*")
def EndUrl():
    elenumSelect1=0
    s1=requests.Session()
    res=s1.get(TicketUrl2)
    soup1 = BeautifulSoup(res.text,"html.parser")
    for ele in soup1.select("input"):
        elenumSelect1=elenumSelect1+1
        if elenumSelect1==3:
            elehref=str(ele)
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

print u"所有票種狀態:"
print AllTicket() 
print u"可以買的票種:"
CanBuyTicket()
print u"請輸入買票代碼:"
UrlGet()
UrlGetList=""
UrlGetList=raw_input().decode(sys.stdin.encoding)
UrlGetList2=int(UrlGetList)
gotoUrl=UrlArray[UrlGetList2-1]
print u"請輸入購買張數"
ticketNum=raw_input().decode(sys.stdin.encoding)

s2=requests.Session()
res=s2.get(gotoUrl)
soup2 = BeautifulSoup(res.text,"html.parser")
for ele in soup2.select("select"):
    eletostr=str(ele)
    eletostr2=eletostr.split("=")[1] 
    eletostr3=eletostr2.split('''"''')[1]
    eletostr4=str(eletostr3)

browser=webdriver.Firefox()
browser.get(gotoUrl)

select = Select(browser.find_element_by_id(eletostr4))
select.select_by_visible_text(ticketNum)
browser.find_element_by_id("ticketPriceSubmit").click()
