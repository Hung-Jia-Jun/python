# coding: utf-8

#網頁爬蟲工具
import requests

#Json轉譯套件
import json

#Debug用套件
import pdb
from CrawlerServer_app.models import TourData

def StartCrawlerTourCorporation(CorporationName,PageIndex):
    
    #設定Session與header
    s = requests.Session()

    #爬取目標旅行社
    SearchNextUrl = 'http://www.'+CorporationName+'.com.tw/EW/Services/SearchListData.asp'


    #pageALL 當前頁數
    #beginDt 查詢起始日
    #endDt   查詢結束日
    data={
    'pageALL':str(PageIndex),
    'beginDt':'2019/03/09',
    'endDt':'2019/09/09'}

    #取得頁面的旅遊資訊  為Json格式
    ReqNextPage = s.post(SearchNextUrl,data = data , timeout=100)

    JsonStr = ReqNextPage.text

    #將文字轉為Json
    PageData = json.loads(JsonStr)



   
    return PageData
