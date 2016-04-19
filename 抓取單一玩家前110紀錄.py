#-*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import MySQLdb
GameNumCodeStr="https://lol.moa.tw/match/show/"
db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="admin",db="lolplayergamedata",charset= 'utf8' )
MySQlQuery=db.cursor() #建立一個供查詢的命令空間
utfCode="""SET NAMES 'utf8'"""
MySQlQuery.execute(utfCode)
db.commit()

def url (ID):
    ID=str(ID)
    res2=requests.get("https://lol.moa.tw/summoner/show/"+ID) #使用者ID網址
    soup = BeautifulSoup(res2.text,"html.parser")
    return soup
def GameAllPlayer (GameNumCode):
    ID_Array=[]
    GameNumCode=str(GameNumCode)
    res2=requests.get(GameNumCodeStr+GameNumCode) #進入詳細資料網址
    PlayerNum=0 #定位其餘十位玩家的位置
    soup = BeautifulSoup(res2.text,"html.parser")
    for ele in soup.select('span'):
        PlayerNum=PlayerNum+1
        if PlayerNum==22:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==26:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==30:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==34:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==38:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==42:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==46:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()
        if PlayerNum==50:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==54:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

        if PlayerNum==58:
            PlayerID=str(ele) #剖析使用者ID
            PlayerID=PlayerID.split(">")[2]
            PlayerID=PlayerID.split("<")[0]
            PlayerID=str(PlayerID)
            print PlayerID
            if PlayerID is "":
                print ""

            else:
                PlayerID="('"+PlayerID+"')"
                MySQL_script="insert into player_id(Player_ID)values"+PlayerID
                MySQlQuery.execute(MySQL_script)
                db.commit()

def GameTotal(SearchNum,SearchUrl):
    res2=requests.get(SearchUrl)
    soup = BeautifulSoup(res2.text,"html.parser")
    SearchNum=(SearchNum-1)*10
    def GameDetail(GameNum):
        recentKDAnum=0
        GameNumCode=0 #對戰定位代號
        if GameNum==3 or 4:
            for ele in soup.select('span'):
                GameNumCode=GameNumCode+1
                ele=str(ele)
                if GameNumCode==((GameNum-1)*10)+3:
                    ele=str(ele)
                    ele=ele.split('>')[1]
                    ele=ele.split('<')[0]
                    print "對戰代號:"+ele

                    GameAllPlayer(ele)

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

            for ele in soup.select('span'):
                GameNumCode=GameNumCode+1
                if GameNumCode==((GameNum-1)*10)+3:
                    ele=str(ele)
                    ele=ele.split('>')[1]
                    ele=ele.split('<')[0]
                    print "對戰代號:"+ele
                    GameAllPlayer(ele)
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
        recentnum=0 #最近對戰的細節定位代號
        LegendNum=0 #英雄定位代號
        for ele in soup.select('td'):
            if LegendNum==11:
                ele=str(ele)
                LegendName=ele.split('''"''')[5]
                print "使用的英雄:"+LegendName
        for ele in soup.select('td'):
            recentnum=recentnum+1
            LegendNum=LegendNum+1
            if LegendNum==((GameNum-1)*10)+1:
                ele=str(ele)
                LegendName=ele.split('''"''')[5]
                print "使用的英雄:"+LegendName
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
def SerchUrl(soup):
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
MySQlQuery.execute("select * from player_id")
for row in MySQlQuery:
    row=str(row)
    row=row.encode('utf-8')
    print row
soup=url("小孩子的把戲")
SerchUrl(soup)
