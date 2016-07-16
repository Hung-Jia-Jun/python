# -*- coding: utf-8 -*-
from socket import *
HOST = 'localhost' #IP位置看  Cmd 輸入指令ipconfig 查看IPv4位置貼上來
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
def WriteSoundTxt(writeTxtInput):
	f = open('C:\\PlaySound_Sync.txt', 'w') #要同步的playsound.txt
	f.write(writeTxtInput)
	f.truncate()
User_Sound=""
def ReadSoundTxt():
	global User_Sound
	for i in open('C:\\PlaySound_Sync.txt','r'):
		User_Sound=i
	if User_Sound=="":
		pass
	return User_Sound
Tempdata=""
while True:
	data=ReadSoundTxt()
	#message = tcpCliSock.recv(BUFSIZ)
	if data=="":
		pass
	else:
		if (data!=Tempdata): #資料較新
			Tempdata=data #將現在的資料存進Tempdata暫存器
			tcpCliSock.send(data)
		#elif (data!=message): #如果client端的資料=data 跟伺服器發送過來的message不一樣的話，就代表來自Server的message資料比較新
		#	WriteSoundTxt(message) #寫入來自server的新資料
		#	print "[Get From Server]:",message
tcpCliSock.close()