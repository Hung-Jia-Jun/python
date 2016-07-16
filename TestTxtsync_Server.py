# -*- coding: utf-8 -*-
from socket import *
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
def WriteSoundTxt(writeTxtInput):
    f = open('C:\\PlaySound.txt', 'w')
    f.write(writeTxtInput)
    f.truncate()
User_Sound=""
def ReadSoundTxt():
    global User_Sound
    for i in open('C:\\PlaySound.txt','r'):
        User_Sound=i
    if User_Sound=="":
        pass
    return User_Sound
Temp_Server_Data=""
while True:
    print 'waiting for connection...'
    tcpCliSock,addr = tcpSerSock.accept()
    print '...connected from: ',addr

    while True:
        #message = raw_input("Service>")
        #tcpCliSock.send(message)
        data = tcpCliSock.recv(BUFSIZ)
        print "[From Client]:",data


        if (data!=Server_Sound_Data): #如果進來的資料=data  跟伺服器Server_Sound_Data不一樣
            Temp_Server_Data=data;#存入暫存器
            WriteSoundTxt(data) #寫入新資料

        Server_Sound_Data=ReadSoundTxt() #伺服器端的Play_Sound.txt


        if (Server_Sound_Data!=Temp_Server_Data)
        #if (Server_Sound_Data!=Temp_Server_Data): #如果今天伺服器這邊的資料比暫存器的資料還新的話
        #    tcpCliSock.send(Server_Sound_Data) #發送較新的數據給Client端
        #    print Server_Sound_Data
tcpSerSock.close()