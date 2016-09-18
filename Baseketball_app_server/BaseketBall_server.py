# -*- coding: utf-8 -*-
from socket import *
import SocketServer,random
from msvcrt import getch

import multiprocessing,os,sys,pdb,time,os,threading
BUFSIZ = 2048  #socket 傳輸單檔大小

py_tcpCliSockarr=[] #User的socket參考陣列
RoomList=[] #the game room list save total online game match,
			#this way can protect all team room not repeat in same
def Get_User_Server():  #管理使用者連接伺服器的陣列
	py_tcpSerSock = socket(AF_INET, SOCK_STREAM)
	py_tcpSerSock.bind(('',31500))
	py_tcpSerSock.listen(50)
	while True:
		print u"等待python客戶端連線...port 31500"
		py_tcpCliSock,addr = py_tcpSerSock.accept()  #連接成功後將連線參考物件推入陣列[0]
		py_tcpCliSockarr.append(py_tcpCliSock)
		print u"python客戶端連線成功"
		SocketLocation=py_tcpCliSockarr.index(py_tcpCliSock)  #Get the Socket Object form Array Position to open new thread argument
		Socket_Ref=py_tcpCliSockarr.pop(SocketLocation) #Select Obj in array and drop it!
		threading.Thread(target=SocketServer,args=(Socket_Ref,)).start() #使用者回應線程

def SocketServer(py_tcpCliSockarr):
	Username="" #使用者帳號
	UserPass="" #使用者密碼
	while True:
		try:
			UserRecv=py_tcpCliSockarr.recv(BUFSIZ) #接收資訊
		except :
			print "The User is disconnect!!!"
			break
		if UserRecv[0:23]=="Login_Facebook_Username":  #如果訊息表頭是Login，就將變數存進使用者帳號
			UserRecv=UserRecv.replace("Login_Facebook_Username","")
			Username=UserRecv
		if UserRecv[0:23]=="Login_Facebook_Password":  #如果訊息表頭是PassWord，就將變數存進使用者密碼
			UserRecv=UserRecv.replace("Login_Facebook_Password","")
			UserPass=UserRecv
		if UserRecv=="Login_Facebook":
			print "Username: ",Username
			print "UserPass: ",UserPass


		#if user want to Create new game Room,Send room password to other user when add this game
		if UserRecv=="Create_Room":  
			Room_num_Stat=""
			Room_Num=random.randint(0,99999)
			while True: #Enter this Loop to Create new room number send to user
				try:
					RoomList.index(Room_Num)  #if the game number is not same other room number,then Create
					Room_num_Stat=False #the Room is same ,need to create new room code
					if Room_num_Stat==False:
						Room_Num=random.randint(0,99999)
				except :
					Room_num_Stat=True #The room Status is no same and then create
					RoomList.append(Room_Num) #append this new game Number
					print "the Game Number is :",Room_Num 
					Room_Num=str(Room_Num) #change Room_Num to string for send client
					py_tcpCliSockarr.send(Room_Num) #send room number
					Room_Num=int(Room_Num) #recover to int 
					break



threading.Thread(target=Get_User_Server).start() #使用者管理線程
