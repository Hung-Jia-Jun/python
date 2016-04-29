#-*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import MySQLdb,pdb
db = MySQLdb.connect("127.0.0.1","root","admin","gamedata")
cursor = db.cursor()
utfCode="""SET NAMES 'utf8'"""
cursor.execute(utfCode)
GameNumCodeStr="https://lol.moa.tw/match/show/"
ID_Array=[]
def url (ID):
    ID=str(ID)#使用者ID
    res2=requests.get("https://lol.moa.tw/summoner/show/"+ID) #使用者ID網址
    soup = BeautifulSoup(res2.text,"html.parser")
    return soup
def GameEquip(soup,EquipNum):
    eleNum=0
    for ele in soup.select("td"):
        eleNum=eleNum+1
        #EquipNum就是我們要查詢那位玩家的前10場對戰的裝備列
        if eleNum==EquipNum:
            print "--------------------------------------------"
            ele=str(ele)
            ele1=ele.split('''data-code="''')[1]
            Equip_ele1=ele1.split('''"''')[0]
            ele2=ele.split('''data-code="''')[2]
            Equip_ele2=ele2.split('''"''')[0]
            ele3=ele.split('''data-code="''')[3]
            Equip_ele3=ele3.split('''"''')[0]
            ele4=ele.split('''data-code="''')[4]
            Equip_ele4=ele4.split('''"''')[0]
            ele5=ele.split('''data-code="''')[5]
            Equip_ele5=ele5.split('''"''')[0]
            ele6=ele.split('''data-code="''')[6]
            Equip_ele6=ele6.split('''"''')[0]
            return Equip_ele1,Equip_ele2,Equip_ele3,Equip_ele4,Equip_ele5,Equip_ele6

def GameAllPlayer (GameNumCode): #查詢所有玩家的ID  存進陣列裡面
    GameNumCode=str(GameNumCode)
    res2=requests.get(GameNumCodeStr+GameNumCode) #進入詳細資料網址
    PlayerNum=0 #定位其餘十位玩家的位置
    soup = BeautifulSoup(res2.text,"html.parser")
    for ele in soup.select('a'):
        PlayerNum=PlayerNum+1
        for i in range(38,48):
            if PlayerNum==i:
                PlayerID=str(ele)
                PlayerID=PlayerID.split("/")[3]
                PlayerID=PlayerID.split('''"''')[0]
                ID_Array.append(PlayerID) #增加進查詢玩家陣列
            #pdb.set_trace()
def GameTotal(SearchNum,SearchUrl,ID_List):
    res2=requests.get(SearchUrl)
    soup = BeautifulSoup(res2.text,"html.parser")
    SearchNum=(SearchNum-1)*10

    GameResult_Num=0 #遊戲結果為1.3.5.7.9.11
    def GameDetail(GameNum,ID_List):
        GameDetail_Array=[] #該場對戰資訊陣列
        if GameNum==1:
            GameResult_Num=1
        if GameNum==2:
            GameResult_Num=3
        if GameNum==3:
            GameResult_Num=5
        if GameNum==4:
            GameResult_Num=7
        if GameNum==5:
            GameResult_Num=9
        if GameNum==6:
            GameResult_Num=11
        if GameNum==7:
            GameResult_Num=13
        if GameNum==8:
            GameResult_Num=15
        if GameNum==9:
            GameResult_Num=17
        if GameNum==10:
            GameResult_Num=19



        recentKDAnum=0
        GameNumCode=0 #對戰定位代號
        if GameNum==3 or 4:
            for ele in soup.select('span'):
                GameNumCode=GameNumCode+1
                ele=str(ele)
                if GameNumCode==((GameNum-1)*10)+3:
                    ele=str(ele)
                    ele=ele.split('>')[1]
                    Game_Num_Code_ele=ele.split('<')[0]
                    print "對戰代號:"+Game_Num_Code_ele
                    Game_Num_Code_ele=str(Game_Num_Code_ele)
                    GameAllPlayer(Game_Num_Code_ele) #將對戰代號推入查詢所有玩家頁面
                    GameDetail_Array.append(Game_Num_Code_ele) #將對戰代號推入陣列中

            for ele in soup.select('tr'):
                recentKDAnum=recentKDAnum+1

                if recentKDAnum==GameResult_Num:
                    ele=str(ele)
                    GameResult=ele.split(">")[5]
                    print "遊戲結果:"+GameResult.split("<")[0]
                    GameResult=GameResult.split("<")[0]
                    GameResult=str(GameResult)
                    GameDetail_Array.append(GameResult)#將遊戲結果推入陣列中

                    GameMap=ele.split(">")[7]
                    print "對戰地圖:"+GameMap.split("<")[0]
                    GameMap=GameMap.split("<")[0]
                    GameMap=str(GameMap)
                    GameDetail_Array.append(GameMap)#將對戰地圖推入陣列中

                    GameStatus=ele.split(">")[9]
                    GameStatus=GameStatus.split("<")[0]
                    print "對戰類型:"+GameStatus
                    GameDetail_Array.append(GameStatus)#將對戰類型推入陣列中
                    GameStatus=GameStatus.split("<")[0]
                    GameStatus=str(GameStatus)

                    #GameTime=ele.split(">")[13]
                    #print "遊戲長度:"+GameTime.split("<")[0]
                    #GameTime=GameTime.split("<")[0]
                    #GameTime=str(GameTime)
                    #GameDetail_Array.append(GameTime)#將遊戲長度推入陣列中

        else:
            for ele in soup.select('span'):
                GameNumCode=GameNumCode+1
                if GameNumCode==((GameNum-1)*10)+3:
                    ele=str(ele)
                    ele=ele.split('>')[1]
                    Game_Num_Code_ele=ele.split('<')[0]
                    print "對戰代號:"+Game_Num_Code_ele
                    Game_Num_Code_ele=str(Game_Num_Code_ele)
                    GameAllPlayer(Game_Num_Code_ele) #將對戰代號推入查詢所有玩家頁面
                    GameDetail_Array.append(Game_Num_Code_ele) #將對戰代號推入陣列中

            for ele in soup.select('tr'):
                recentKDAnum=recentKDAnum+1
                if recentKDAnum==GameResult_Num:
                    ele=str(ele)
                    GameResult=ele.split(">")[5]
                    print "遊戲結果:"+GameResult.split("<")[0]
                    GameResult=GameResult.split("<")[0]
                    GameResult=str(GameResult)
                    GameDetail_Array.append(GameResult)#將遊戲結果推入陣列中

                    GameMap=ele.split(">")[7]
                    print "對戰地圖:"+GameMap.split("<")[0]
                    GameMap=GameMap.split("<")[0]
                    GameMap=str(GameMap)
                    GameDetail_Array.append(GameMap)#將對戰地圖推入陣列中

                    GameStatus=ele.split(">")[9]
                    GameStatus=GameStatus.split("<")[0]
                    print "對戰類型:"+GameStatus
                    GameDetail_Array.append(GameStatus)#將對戰類型推入陣列中

                    ##GameTime=ele.split(">")[13]
                    ##print "遊戲長度:"+GameTime.split("<")[0]
                    ##GameTime=GameTime.split("<")[0]
                    ##GameTime=str(GameTime)
                    ##GameDetail_Array.append(GameTime)#將遊戲長度推入陣列中
        GameEquip_Content=GameEquip(soup,((GameNum-1)*10+4))
        #4=查詢第一場角色裝備
        #14=查詢第二場角色裝備
        #24=查詢第三場角色裝備.....etc
        try:
            GameEquip_1=GameEquip_Content[0]
            GameEquip_2=GameEquip_Content[1]
            GameEquip_3=GameEquip_Content[2]
            GameEquip_4=GameEquip_Content[3]
            GameEquip_5=GameEquip_Content[4]
            GameEquip_6=GameEquip_Content[5]
            GameDetail_Array.append(GameEquip_1)
            GameDetail_Array.append(GameEquip_2)
            GameDetail_Array.append(GameEquip_3)
            GameDetail_Array.append(GameEquip_4)
            GameDetail_Array.append(GameEquip_5)
            GameDetail_Array.append(GameEquip_6)
        except :
            pass
        recentnum=0 #最近對戰的細節定位代號
        LegendNum=0 #英雄定位代號
        for ele in soup.select('td'):
            recentnum=recentnum+1
            LegendNum=LegendNum+1
            if LegendNum==((GameNum-1)*10)+1:
                ele=str(ele)
                LegendName=ele.split('''"''')[5]
                print "使用的英雄:"+LegendName
                GameDetail_Array.append(LegendName)

            if recentnum==((GameNum-1)*10)+2:
                ele=str(ele)
                print "擊殺:"+ele.split('''"''')[7]
                Kill=ele.split('''"''')[7] #擊殺
                GameDetail_Array.append(Kill)

                print "死亡:"+ele.split('''"''')[11]
                Death=ele.split('''"''')[11] #死亡
                GameDetail_Array.append(Death)

                print "助攻:"+ele.split('''"''')[15]
                A=ele.split('''"''')[15] #助攻
                GameDetail_Array.append(A)

                KDAScroe=ele.split('''(''')[1]
                KDAScroe=KDAScroe.split(''')''')[0]
                print "KDA值:"+KDAScroe
                GameDetail_Array.append(KDAScroe)

        GameDetail_Len=len(GameDetail_Array)
        GameDetail_Len=int(GameDetail_Len)
        for i in range(0,GameDetail_Len):
            print GameDetail_Array[i]
        try:
            This_Game_Result=GameDetail_Array[1]
            PlayerMap=GameDetail_Array[2]
            PlayClass=GameDetail_Array[3]
            Equip_1=GameDetail_Array[4]
            Equip_2=GameDetail_Array[5]
            Equip_3=GameDetail_Array[6]
            Equip_4=GameDetail_Array[7]
            Equip_5=GameDetail_Array[8]
            Equip_6=GameDetail_Array[9]
            UserHero=GameDetail_Array[10]
            Kill=GameDetail_Array[11]
            Death=GameDetail_Array[12]
            A=GameDetail_Array[13]
            KDANum=GameDetail_Array[14]
            sql="insert into lol_player_database(玩家ID,使用的英雄,裝備_1,裝備_2,裝備_3,裝備_4,裝備_5,裝備_6,遊戲結果,對戰地圖,對戰類型,擊殺,死亡,助攻,KDA值)values('"+ID_List+"','"+UserHero+"','"+Equip_1 +"','"+ Equip_2+"','"+Equip_3 +"','"+Equip_4 +"','"+ Equip_5+"','"+Equip_6 +"','"+This_Game_Result+"','"+PlayerMap+"','"+PlayClass +"','"+Kill +"','"+Death+"','"+A+"','"+KDANum+"');"
            print sql
            cursor.execute(sql)
            db.commit()
        except :
            pass
    for i in range(1,11):
        GameNumber=SearchNum+i
        GameNumber=str(GameNumber)
        print GameNumber+"-------------------------------"
        GameDetail(i,ID_List) #對所有對戰資訊做查詢##
        print "-------------------------------"
def SerchUrl(soup,ID_List):
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
                GameTotal(SearchNum,SearchUrl,ID_List)  #SearchNum是搜尋次數，用來方便做出0~100的對戰紀錄，否則只會一直1~10重複10次

soup=url("我")
SerchUrl(soup,"我")
while True:
    startList=0
    ID_Len=len(ID_Array)
    ID_Len=int(ID_Len)
    for i in range (startList,ID_Len):
        ID_List=ID_Array[i]
        ID_List=str(ID_List)
        soup=url(ID_List)
        SerchUrl(soup,ID_List)
        #pdb.set_trace()
        if i==ID_Len: #如果迴圈數=陣列元素內的所有值
            startList=i #就將目前運行中的迴圈數存進陣列起始值
            print "startList:"+startList
