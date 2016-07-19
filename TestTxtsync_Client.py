# -*- coding: utf-8 -*-
from socket import *
import multiprocessing,pdb
User_Sound=""
BUFSIZ = 1024

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

def RunThread(SocketTo):
	PlaySound_console=WriteSoundTxt('C:\\A_Client.txt',"") #伺服器端的A.txt辨識指令檔
	Server_Sound_Data=WriteSoundTxt('C:\\PlaySound_Client.txt',"") #伺服器端的Play_Sound.txt
	WriteSoundTxt('C:\\RecogContant_Client.txt',"")#寫入新資料



	PORT = 47990
	ADDR = (SocketTo,PORT) #IP位置看  Cmd 輸入指令ipconfig 查看IPv4位置貼上來
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	Tempdata=""
	Console_Tempdata=""
	Temp_RecogContant=""
	while True:
		#pdb.set_trace()

		Recv_Server_Message=tcpCliSock.recv(BUFSIZ) #接收server指令
		tcpCliSock.send(" ")#發送空值不然server會一直等待

		if Recv_Server_Message[0:10]=="Sound_Data":
			message=Recv_Server_Message.split("Sound_Data")[1]
			if (Tempdata!=message): #如果server給的資料與現在的暫存器內容不一樣
				print u"[Server PlaySound ]: "+message
				Tempdata=message #將現在的資料存進Tempdata暫存器
				WriteSoundTxt('C:\\PlaySound_Client.txt',message)#寫入新資料

		elif Recv_Server_Message[0:17]=="Playsound_console":
			Console_Message=Recv_Server_Message.split("Playsound_console")[1]
			if (Console_Tempdata!=Console_Message): #如果server給的資料與現在的暫存器內容不一樣
				print u"[Server python Console]: "+Console_Message
				Console_Tempdata=Console_Message #將現在的資料存進Tempdata暫存器
				WriteSoundTxt('C:\\A_Client.txt',Console_Message)#寫入新資料




		RecogContant=ReadSoundTxt('C:\\RecogContant_Client.txt') #client端的辨識結果要回傳給server 所以一直去讀取辨識結果內容
		if RecogContant=="":
		    pass
		else:
		    if (RecogContant!=Temp_RecogContant): #如果發送前的資料 與上次發送的內容部不一樣
		        Temp_RecogContant=RecogContant;#把現在這個較新的資料存入暫存器
		        print "RecogContant Send..."
		        try:
		            tcpCliSock.send("RecogContant"+RecogContant) #發送更新的伺服器發聲命令
		        except :
		            pass




	tcpCliSock.close()
if __name__ == '__main__':
	print u"[遠端連線的主機] : "
	#SocketTo="localhost"
	#SocketTo=raw_input()
	SocketTo="163.18.62.27"
	RunThread(SocketTo)
