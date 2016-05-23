#-*- coding: utf8 -*-
import socks,socket,Queue
from bs4 import BeautifulSoup
import requests,sys,time
import MySQLdb,pdb,random
socks.setdefaultproxy(socks.SOCKS5, '127.0.0.1', 9150, True)
socket.socket = socks.socksocket

res2=requests.get("http://dir.twseo.org/ip-check.php")
soup = BeautifulSoup(res2.text,"html.parser")

elenum=0
for i in soup.select("font"):
    elenum=elenum+1
    if elenum==2:
        IPStr=soup.text
        IPStr=IPStr.split(":")[1]
        IPStr=IPStr.split("IP")[0]
        IPStr=IPStr.split(" ")[1]
        print IPStr