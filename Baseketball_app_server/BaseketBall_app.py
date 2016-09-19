# -*- coding: utf-8 -*-
from socket import *
import multiprocessing,pdb,sys,os,threading
from msvcrt import getch
User_Sound=""
BUFSIZ = 2048
os.system("chcp 950")  #設定字碼頁
RecvData=""
Room_Code="" #The user Room_codeee
def Recv_Data(tcpCliSock_ref):
	global RecvData,Room_Code
	while True:
		try:
			RecvData=tcpCliSock_ref.recv(BUFSIZ)
			if RecvData[0:7]=="RoomNum":
				Room_Code=RecvData.replace("RoomNum","")
				print "The Room number is :",Room_Code
			if RecvData[0:13]=="RoomBroadcast":
				GetRoomCode=RecvData.split("|")[1]
				GetRoomMsg=RecvData.split("|")[2]
				#if GetRoomCode==Room_Code: #if Get server send Room message ,check the room code
				print "RoomMsg is : ",GetRoomMsg
		except :
			pass
def RunThread():
	global Room_Code
	SocketTo="localhost"  #遠端server  要改
	PORT = 31500 #轉送python Client端的port
	ADDR = (SocketTo,PORT)
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)


	Username=""
	UserPass=""
	print "Username: "
	#Username=raw_input()

	print "UserPass: "
	#UserPass=raw_input()
	threading.Thread(target=Recv_Data,args=(tcpCliSock,)).start() #使用者回應線程


	#Recv_Server_Message=tcpCliSock.recv(BUFSIZ) #接收server指令
	SendName="Login_Facebook_Username"+Username
	SendPass="Login_Facebook_Password"+UserPass
	tcpCliSock.send(SendName)
	tcpCliSock.send(SendPass)
	tcpCliSock.send("Login_Facebook")
	print "1.Create Room  2.Enter Room"
	Room_Mode=raw_input()
	if Room_Mode=="1": #Create Room Mode to tell server Create Room wait to user enter
		tcpCliSock.send("Create_Room") #創建房間
		print "Create_Room"
	if Room_Mode=="2":
		Room_Code=raw_input() #User input the room number to Enter Created Room
		EnterRoom="Enter_Room"+Room_Code #Add this string "Enter_Room" to tell server Search Room code
		tcpCliSock.send(EnterRoom) #創建房間
	while True:
		#if RecvData=="RoomBroadcast":
		print "Input Room Talk:　" #Talk same room other user message
		Room_Talk=raw_input()
		Room_Talk="RoomBroadcast"+"|"+Room_Code+"|"+Room_Talk #Send server Room Code and Message to other Player
		tcpCliSock.send(Room_Talk)
if __name__ == '__main__':  #如果執行的是本體的話，才執行下面的語句
	threading.Thread(target=RunThread).start()
