# -*- coding: utf-8 -*-
from socket import *
import multiprocessing,os,sys,pdb
BUFSIZ=1024
User_Sound=""




def WriteSoundTxt(FileLocation,writeTxtInput):
        f = open(FileLocation, 'w') #要同步的playsound.txt
        f.write(writeTxtInput)
        f.close() #關閉文件流
def ReadSoundTxt(FileLocation):
    global User_Sound
    for i in open(FileLocation,'r'):
        User_Sound=i
    if User_Sound=="":
        pass
    return User_Sound

def RunThread():
    PlaySound_console=WriteSoundTxt('C:\\A.txt',"") #伺服器端的A.txt辨識指令檔
    Server_Sound_Data=WriteSoundTxt('C:\\PlaySound.txt',"") #伺服器端的Play_Sound.txt
    WriteSoundTxt('C:\\RecogContant.txt',"")#寫入新資料

    HOST = ''
    PORT = 47990

    ADDR = (HOST,PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    User_Sound=""
    Temp_Server_Data=""
    Temp_Sound_Console=""
    Temp_RecogContant=""
    Recv_Client_Message=""
    Tempdata=""
    while True:
        #pdb.set_trace()
        print 'waiting for Client connection...'
        tcpCliSock,addr = tcpSerSock.accept()
        print 'connected Client from: ',addr,".................."
        while True:
            #pdb.set_trace()

            try:
                tcpCliSock.send(" ")#測試connet狀態
                Recv_Client_Message=tcpCliSock.recv(BUFSIZ) #接收Client python指令
                if Recv_Client_Message=="Clinet Connet":
                    Recv_Client_Message=""
            except:
                break #進入等待client的迴圈等待連線

            PlaySound_console=ReadSoundTxt('C:\\A.txt') #伺服器端的A.txt辨識指令檔
            Server_Sound_Data=ReadSoundTxt('C:\\PlaySound.txt') #伺服器端的Play_Sound.txt
            if Server_Sound_Data=="":
                pass
            else:
                if (Server_Sound_Data!=Temp_Server_Data): #如果發送前的資料 與上次發送的內容部不一樣
                    Temp_Server_Data=Server_Sound_Data;#把現在這個較新的資料存入暫存器
                    #Server_Sound_Data="Sound_Data"+Server_Sound_Data
                    print "Sound_Data Send..."
                    try:
                        tcpCliSock.send("Sound_Data"+Server_Sound_Data) #發送更新的伺服器發聲資料
                    except :
                        pass


            if PlaySound_console=="":
                pass
            else:
                if (PlaySound_console!=Temp_Sound_Console): #如果發送前的資料 與上次發送的內容部不一樣
                    Temp_Sound_Console=PlaySound_console;#把現在這個較新的資料存入暫存器
                    print "Playsound_console Send..."
                    try:
                        tcpCliSock.send("Playsound_console"+PlaySound_console) #發送更新的伺服器發聲命令
                    except :
                        pass



            if Recv_Client_Message[0:12]=="RecogContant":
                message=Recv_Client_Message.split("RecogContant")[1]
                if (Tempdata!=message): #如果server給的資料與現在的暫存器內容不一樣
                    print u"Get RecogContant~ "
                    Tempdata=message #將現在的資料存進Tempdata暫存器
                    WriteSoundTxt('C:\\RecogContant.txt',message)#寫入新資料










    tcpSerSock.close()





RunThread()

