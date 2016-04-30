#coding=utf-8
import requests
import urllib2
from bs4 import BeautifulSoup
import string,sys,re,io,os,pdb
from requests import Request, Session
import time
s2=requests.Session()
res=s2.get("https://tixcraft.com/ticket/area/16_DellaKH/1220")
soup2 = BeautifulSoup(res.text,"html.parser")
TickNumber=0
scriptNum=0
userfindWord1="橙208區在一起雙人套票"
UrlArray=[]
def GetTickUrl():
    elenum=0
    for ele in soup2.select("script"):
        eleurl=ele.text
    eleurl2=eleurl.split("{")[8]
    eleurl3=eleurl2
    eleurl3=eleurl2.split(":")
    elenumlist=0
    for i in range(100,0,-1):
        elenumlist=elenumlist+1
        eleurl4=eleurl3[elenumlist]
        eleurl5=OnlyCharNum(eleurl4)
        eleurl6=eleurl5.split('''"''')[1]
        url="https://tixcraft.com"+eleurl6
        UrlArray.append(url)
for ele in soup2.select('li'):
    TickNumber=TickNumber+1
    select_ele=len(soup2.select('li'))
    select_ele=int(select_ele)+1
    for i in range(10,select_ele):
        if TickNumber==i:
            ele=str(ele)
            if ele.find(userfindWord1)>0:
                TickName_ele=ele.split('''"''')[3]
                #print TickName_ele
                TickName_ele=str(TickName_ele)
GetTickUrl()
    #print ele
    #ele=str(ele)
    #ele2=ele.split("""{""")[10]
    #print ele2
