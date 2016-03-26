#coding=utf-8
import requests
import urllib2
from bs4 import BeautifulSoup
import string,sys,re,io,os
from requests import Request, Session
import time
UrlArray=[]
findList=[]
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
        elenumlist=0
        for i in range(100,0,-1):
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
    ArrayLen=0

    for ele in soup.select("li"):
        elenum=elenum+1
        if elenum>9:
            find_ele=ele.text
            if find_ele.find(findWord)<0:#找尋是否有"已賣完"的關鍵字，有的話就顯示在可購買的列表中
                eleencode=ele.text
                eleencode2=eleencode.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)#將ASCII中不認識的字元替換成"?"
                eleTicket=eleencode2.replace("?","*")#將替換後的值存給eleTicket
                ArrayLen=ArrayLen+1
                if eleTicket.find(userfindWord1) >0:
                    print u"已找到",userfindWord1,u"這張票的位置"
                    findList.append([ArrayLen-1])#在陣列中追加找到的位置，以便打開網頁
def EndUrl():#剖析使用者輸入的網頁內是否有"立即購票"連結
    isUrlOpen=False
    elenumSelect1=0
    s1=requests.Session()
    while isUrlOpen==False:
        try:
            res2=s1.get(TicketUrl2)
            soup1 = BeautifulSoup(res2.text,"html.parser")

            for ele in soup1.select("input"):
                elenumSelect1=elenumSelect1+1
                if elenumSelect1==3:
                    elehref=str(ele)
                    elehref=elehref[18:100]
                    elehref=elehref.split('''"''')[0]
                    eleEndUrl="https://tixcraft.com"+elehref
                    eleEndUrl=str(eleEndUrl)
                    print u"查看是否可以開啟購票網頁中......"
                    print ""
                    returnUrl="https://tixcraft.com/ticket/area/16_SNSD/1231"
                    isUrlOpen==True
                    return str(returnUrl)
                    res=requests.get(returnUrl)#如果錯誤的話會跳到還沒開始購票的except
                    #print u"已開放購票"
                    #print ""
                    #return str(eleEndUrl)
        except :
            isUrlOpen==False
            print u"還沒開始購票"
            print ""
            while isUrlOpen==False:
                     isUrlOpen=EndUrl()
    pass


isbreak=0
ReturnUrl_intNum=0

tmpList=0
print u"請選擇購票模式:"
print u"1  已開放購票需要搶票"
print u"2  未開放購票，需讓程式等待"
TicketMode=raw_input().decode(sys.stdin.encoding)
TicketMode=int(TicketMode)
if TicketMode==1:
    print u"已開放購票需要搶票模式開啟"
    print u"請將網頁背景的cookie貼上來"
    GetCSRF=raw_input().decode(sys.stdin.encoding)
    GetCSRF=str(GetCSRF)
    GetSID=GetCSRF.split("SID=")[1]
    SID=GetSID.split(";")[0]
    GetCSRF=GetCSRF.split("CSRFTOKEN=")[1]
    CSRF=GetCSRF.split(";")[0]

    GetCookie={
        "SID":SID,
        "CSRFTOKEN":CSRF,
    }

    findWord="已售完"
    findWord=findWord.decode("utf-8")
    print u"請輸入購票網址:"
    TicketUrl=raw_input().decode(sys.stdin.encoding)
    TicketUrl2=TicketUrl.replace("detail","game")
    print u"請輸入指定票種:"
    userfindWord1=raw_input().decode(sys.stdin.encoding)
    print u"請輸入購買張數"
    ticketNum=raw_input().decode(sys.stdin.encoding)
    print u"剖析購票網址中......."

    eleEndUrl=EndUrl()
    s4=requests.Session()
    res=s4.get(eleEndUrl)
    soup = BeautifulSoup(res.text,"html.parser")
    print u"查找能購票的網址中是否有使用者的關鍵字......"
    print ""
    CanBuyTicket()
    UrlGet()

    CSRFGet=0
    gotoUrlnum=findList[0]#將取得的list陣列存入變數以便轉換為int
    print u"將",userfindWord1,u"這張票的網址轉換中...."
    print ""
    gotoUrlnum=magic(gotoUrlnum)#轉換list變成int
    gotoUrl=UrlArray[gotoUrlnum]
    s2=requests.Session()
    print u"剖析網頁中",userfindWord1,u"這張票確認購買的按鈕ID，然後等待傳送"
    print ""
    res=s2.get(gotoUrl,cookies=GetCookie)
    soup2 = BeautifulSoup(res.text,"html.parser")
    for ele in soup2.select("input"):
        CSRFGet=CSRFGet+1
        if CSRFGet ==2:
            ele=str(ele)
            ele=ele.split("=")[4]
            ele=ele.replace("/>","")
            ele2str=ele.replace('''"''',"")
        for ele in soup2.select("select"):#剖析網頁中"確認購買"的按鈕ID
            eletostr=str(ele)
            eletostr=eletostr.split("=")[1]
            eletostr=eletostr.split('''"''')[1]
            eletostr=eletostr.replace("TicketForm_ticketPrice_","")
            eletostr="TicketForm[ticketPrice]["+eletostr+"]"
    print u"已找到按鈕ID，ID名稱為:"+eletostr
    print ""








    datas={
        "CSRFTOKEN":ele2str,
        eletostr:ticketNum,
        "yt":"確認張數"
    }
    s=requests.Session()
    tStart=time.time()#計時開始------------------------------------------------------------
    print u"--------------------------------------購票計時開始------------------------------------------------------------"
    print u"傳送購票資訊中....."
    print ""
    res=s.post(gotoUrl,data=datas,cookies=GetCookie)
    print u"等待購票伺服器返回中....."
    print ""
    res5=s.get("https://tixcraft.com/ticket/check",cookies=GetCookie)
    print u"購買完成"
    tEnd=time.time()  #計時結束------------------------------------------------------------
    print u"--------------------------------------購票計時結束------------------------------------------------------------"
    TotalTime=str(tEnd - tStart)
    print u"購票時間一共"+TotalTime,u"秒"
    print ""
    print u"按下enter結束"
    raw_input().decode(sys.stdin.encoding)
if TicketMode==2:
    print u"未開放購票，需讓程式等待模式開啟"
    print u"請將網頁背景的cookie貼上來"
    GetCSRF=raw_input().decode(sys.stdin.encoding)
    GetCSRF=str(GetCSRF)
    GetSID=GetCSRF.split("SID=")[1]
    SID=GetSID.split(";")[0]
    GetCSRF=GetCSRF.split("CSRFTOKEN=")[1]
    CSRF=GetCSRF.split(";")[0]

    GetCookie={
        "SID":SID,
        "CSRFTOKEN":CSRF,
    }

    findWord="已售完"
    findWord=findWord.decode("utf-8")
    print u"請輸入購票網址:"
    TicketUrl=raw_input().decode(sys.stdin.encoding)
    TicketUrl2=TicketUrl.replace("detail","game")
    print u"請輸入指定票種:"
    userfindWord1=raw_input().decode(sys.stdin.encoding)
    print u"請輸入購買張數"
    ticketNum=raw_input().decode(sys.stdin.encoding)
    print u"剖析購票網址中......."

    eleEndUrl=EndUrl()
    s4=requests.Session()
    res=s4.get(eleEndUrl)
    soup = BeautifulSoup(res.text,"html.parser")
    print u"查找能購票的網址中是否有使用者的關鍵字......"
    print ""
    CanBuyTicket()
    UrlGet()

    CSRFGet=0
    gotoUrlnum=findList[0]#將取得的list陣列存入變數以便轉換為int
    print u"將",userfindWord1,u"這張票的網址轉換中...."
    print ""
    gotoUrlnum=magic(gotoUrlnum)#轉換list變成int
    gotoUrl=UrlArray[gotoUrlnum]
    s2=requests.Session()
    print u"剖析網頁中",userfindWord1,u"這張票確認購買的按鈕ID，然後等待傳送"
    print ""
    res=s2.get(gotoUrl,cookies=GetCookie)
    soup2 = BeautifulSoup(res.text,"html.parser")
    for ele in soup2.select("input"):
        CSRFGet=CSRFGet+1
        if CSRFGet ==2:
            ele=str(ele)
            ele=ele.split("=")[4]
            ele=ele.replace("/>","")
            ele2str=ele.replace('''"''',"")
        for ele in soup2.select("select"):#剖析網頁中"確認購買"的按鈕ID
            eletostr=str(ele)
            eletostr=eletostr.split("=")[1]
            eletostr=eletostr.split('''"''')[1]
            eletostr=eletostr.replace("TicketForm_ticketPrice_","")
            eletostr="TicketForm[ticketPrice]["+eletostr+"]"
    print u"已找到按鈕ID，ID名稱為:"+eletostr
    print ""








    datas={
        "CSRFTOKEN":ele2str,
        eletostr:ticketNum,
        "yt":"確認張數"
    }
    s=requests.Session()
    tStart=time.time()#計時開始------------------------------------------------------------
    print u"--------------------------------------購票計時開始------------------------------------------------------------"
    print u"傳送購票資訊中....."
    print ""
    res=s.post(gotoUrl,data=datas,cookies=GetCookie)
    print u"等待購票伺服器返回中....."
    print ""
    res5=s.get("https://tixcraft.com/ticket/check",cookies=GetCookie)
    print u"購買完成"
    tEnd=time.time()  #計時結束------------------------------------------------------------
    print u"--------------------------------------購票計時結束------------------------------------------------------------"
    TotalTime=str(tEnd - tStart)
    print u"購票時間一共"+TotalTime,u"秒"
    print ""
    print u"按下enter結束"
    raw_input().decode(sys.stdin.encoding)
