#coding=utf-8
import requests
import urllib2
from bs4 import BeautifulSoup
import string,sys,re,io,os
from tqdm import tqdm
from requests import Request, Session
from  urllib  import  quote
isbreak=0
ReturnUrl_intNum=0
UrlArray=[]
findList=[]
tmpList=0
print u"請將網頁背景的cookie貼上來"


GetCSRF=raw_input().decode(sys.stdin.encoding)
GetCSRF=str(GetCSRF)
GetSID=GetCSRF.split("SID=")[1]
SID=GetSID.split(";")[0]

GetCSRF=GetCSRF.split("CSRFTOKEN=")[1]
CSRF=GetCSRF.split(";")[0]




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
                eleTicket=eleencode2.replace("?","*")#將替換後的值存給eleTicket
                ArrayLen=ArrayLen+1
                if eleTicket.find(userfindWord1) >0:
                    ReturnUrl_intNum=ArrayLen-1    #如果發現使用者輸入的關鍵字就將目前陣列位置回傳出
                    findList.append([ReturnUrl_intNum])#在陣列中追加找到的位置，以便打開網頁

def EndUrl():#剖析使用者輸入的網頁內是否有"立即購票"連結
    isUrlOpen=False
    elenumSelect1=0
    s1=requests.Session()
    res2=s1.get(TicketUrl2)
    soup1 = BeautifulSoup(res2.text,"html.parser")

    for ele in soup1.select("input"):
        elenumSelect1=elenumSelect1+1
        if elenumSelect1==3:
            elehref=str(ele)
    elehref=elehref[18:100]
    elehref=elehref.split('''"''')[0]
    eleEndUrl="https://tixcraft.com"+elehref
    isUrlOpen==True
    return str(eleEndUrl)

GetCookie={
    "SID":SID,
    "CSRFTOKEN":CSRF,
}

EndUrl()
eleEndUrl=EndUrl()
s4=requests.Session()
res=s4.get(eleEndUrl)
soup = BeautifulSoup(res.text,"html.parser")
findWord="已售完"
findWord=findWord.decode("utf-8")
CanBuyTicket()
UrlGet()
CSRFGet=0
gotoUrlnum=findList[0]#將取得的list陣列存入變數以便轉換為int
gotoUrlnum=magic(gotoUrlnum)#轉換list變成int
gotoUrl=UrlArray[gotoUrlnum]
s2=requests.Session()
res=s2.get(gotoUrl,cookies=GetCookie)
soup2 = BeautifulSoup(res.text,"html.parser")
for ele in soup2.select("input"):
    CSRFGet=CSRFGet+1
    if CSRFGet ==2:
        ele2=str(ele)
        ele3=ele2.split("=")[4]
        ele4=ele3.replace("/>","")
        ele5=ele4.replace('''"''',"")

for ele in soup2.select("select"):#剖析網頁中"確認購買"的按鈕ID
    eletostr=str(ele)
    eletostr2=eletostr.split("=")[1]
    eletostr3=eletostr2.split('''"''')[1]
    eletostr4=eletostr3
    eletostr5=eletostr4.replace("TicketForm_ticketPrice_","")
    eletostr6="TicketForm[ticketPrice]["+eletostr5+"]"
datas={
    "CSRFTOKEN":ele5,
    eletostr6:ticketNum,
    "yt":"確認張數"
}
s=requests.Session()
res=s.post(gotoUrl,data=datas,cookies=GetCookie)
res5=s.get("https://tixcraft.com/ticket/check",cookies=GetCookie)
print u"購買完成"
