# -*- coding: utf-8 -*-
from socket import *
import multiprocessing,pdb,sys,os
from msvcrt import getch
User_Sound=""
BUFSIZ = 1024
os.system("chcp 950")  #設定字碼頁

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



	PORT = 47991
	ADDR = (SocketTo,PORT) #IP位置看  Cmd 輸入指令ipconfig 查看IPv4位置貼上來
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	Tempdata=""
	Console_Tempdata=""
	Temp_RecogContant=""
	Temp_Recv_data=""  #暫存的Recv Data
	while True:
		#pdb.set_trace()
		print "Python Client"
		#tcpCliSock.send("Python Client")
		Recv_Server_Message=tcpCliSock.recv(BUFSIZ) #接收server指令
		print "user:",Recv_Server_Message

		if Recv_Server_Message[0:21]=="Send_To_PythonClient:": #當接收到server專屬傳給python Client的字串時
			Recv_Server_Message=Recv_Server_Message.replace("Send_To_PythonClient:","").strip() #替換掉特徵字元  "Send_To_PythonClient"
			if Temp_Recv_data!=Recv_Server_Message:
				Temp_Recv_data=Recv_Server_Message
				Client_Console=Recv_Server_Message.split(",")[0]
				Language=Recv_Server_Message.split(",")[1]
				Message=Recv_Server_Message.split(",")[2]
				os.system("cls")
				print "Client_Console : ",Client_Console #顯示命令
				if 	Client_Console=="1"
					WriteSoundTxt('C:\\A_Client.txt',"1") #伺服器端的A.txt辨識指令檔
				print "Language : ",Language
				print "Message: ",Message
				print "------------------------------------"
				#pdb.set_trace()
				#sys.exit()

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
	SocketTo="localhost"
	RunThread(SocketTo)
