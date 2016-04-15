from bs4 import BeautifulSoup
import requests

res2=requests.get("https://lol.moa.tw/summoner/show/台灣狗狗") #使用者ID網址

soup = BeautifulSoup(res2.text,"html.parser") 
def GameTotal(SearchNum,SearchUrl):
    res2=requests.get(SearchUrl)
    soup = BeautifulSoup(res2.text,"html.parser")
    SearchNum=(SearchNum-1)*10
    def GameDetail(GameNum):
        recentKDAnum=0
        if GameNum==3 or 4:
            for ele in soup.select('tr'):
                recentKDAnum=recentKDAnum+1
                if recentKDAnum==1:
                    ele=str(ele)
                    GameResult=ele.split(">")[5]
                    print "遊戲結果:"+GameResult.split("<")[0]

                    GameMap=ele.split(">")[7]
                    print "對戰地圖:"+GameMap.split("<")[0]

                    GameStatus=ele.split(">")[9]
                    print "對戰類型:"+GameStatus.split("<")[0]

                    GameTime=ele.split(">")[13]
                    print "遊戲長度:"+GameTime.split("<")[0]
        else:
            for ele in soup.select('tr'):
                recentKDAnum=recentKDAnum+1
                if recentKDAnum==((GameNum-1)*10)+1:
                    ele=str(ele)
                    GameResult=ele.split(">")[5]
                    print "遊戲結果:"+GameResult.split("<")[0]

                    GameMap=ele.split(">")[7]
                    print "對戰地圖:"+GameMap.split("<")[0]

                    GameStatus=ele.split(">")[9]
                    print "對戰類型:"+GameStatus.split("<")[0]

                    GameTime=ele.split(">")[13]
                    print "遊戲長度:"+GameTime.split("<")[0]
        recentnum=0
        for ele in soup.select('td'):
            recentnum=recentnum+1
            if recentnum==((GameNum-1)*10)+2:
                ele=str(ele)
                print "擊殺:"+ele.split('''"''')[7]
                print "死亡:"+ele.split('''"''')[11]
                print "助攻:"+ele.split('''"''')[15]
                KDAScroe=ele.split('''(''')[1]
                KDAScroe=KDAScroe.split(''')''')[0]
                print "KDA值:"+KDAScroe
    for i in range(1,11):
        GameNumber=SearchNum+i
        GameNumber=str(GameNumber)
        print GameNumber+"-------------------------------"
        GameDetail(i)
        print "-------------------------------"
def SerchUrl():
    urlStr="https://lol.moa.tw/Ajax/recentgames/"
    urlnum=0 #要剖析的定位行數，利用他到達指定行數後即停止，即可剖析查詢網址
    pagenum=0 #顯示更多對戰的頁碼
    SearchNum=0 #搜尋次數
    for ele in soup.select('li'):  #網址在li這個欄位內 
        urlnum=urlnum+1
        if urlnum==43:  #定位到第43個li欄位中即是該玩家的近期對戰資料網址
            ele=str(ele) #轉成文字類型
            eleUrl=ele.split("=")[2]
            urlStr=urlStr+eleUrl[17:25]
            for pagenum in range(0,11):
                pagenum=str(pagenum)
                SearchNum=SearchNum+1
                SearchUrl=urlStr+"/page:"+pagenum+"/sort:GameMatch.createDate/direction:desc"
                SearchUrl=str(SearchUrl)
                GameTotal(SearchNum,SearchUrl)  #SearchNum是搜尋次數，用來方便做出0~100的對戰紀錄，否則只會一直1~10重複10次
                print SearchUrl
SerchUrl()
