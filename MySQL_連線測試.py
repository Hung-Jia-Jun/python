#-*- coding: utf8 -*-
import MySQLdb,sys
db = MySQLdb.connect("127.0.0.1","root","admin","gamedata")
cursor = db.cursor()
strcode="我是werwer"
utfCode="""SET NAMES 'utf8'"""
cursor.execute(utfCode)
sql="insert into lol_player_data(玩家ID,使用的英雄,裝備_1,裝備_2,裝備_3,裝備_4,裝備_5,裝備_6,遊戲結果,對戰地圖,對戰類型,擊殺,死亡,助攻,KDA值)values('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15');"
print sql
cursor.execute(sql)
db.commit()
