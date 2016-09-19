# -*- coding: utf-8 -*-
from socket import *
import SocketServer,random,pdb
from msvcrt import getch
import numpy
import multiprocessing,os,sys,pdb,time,os,threading
BUFSIZ = 2048  #socket 傳輸單檔大小

py_tcpCliSockarr=[] #User的socket參考陣列
RoomList=[] #the game room list save total online game match,
			#this way can protect all team room not repeat in same


UserRecv="" #the user reciver to server save in this string


def Get_User_Server():  #管理使用者連接伺服器的陣列
	py_tcpSerSock = socket(AF_INET, SOCK_STREAM)
	py_tcpSerSock.bind(('',31500))
	py_tcpSerSock.listen(50)
	while True:
		print u"Wait for user connect listen the 31500 of port...."
		py_tcpCliSock,addr = py_tcpSerSock.accept()  #連接成功後將連線參考物件推入陣列[0]
		py_tcpCliSockarr.append(py_tcpCliSock) #add user socket refence to pop array
		print u"Is user connected!!!"
		SocketLocation=py_tcpCliSockarr.index(py_tcpCliSock)  #Get the Socket Object form Array Position to open new thread argument
		Socket_Ref=py_tcpCliSockarr.pop(SocketLocation) #Select Obj in array and drop it!
		threading.Thread(target=SocketServer,args=(Socket_Ref,)).start() #使用者回應線程



Game_Room_soc=[]   #In this room ,player socket reference in here
for i in range(99999): #Declare(Talk Computer of programer) the Socket Array
	Newlist=[0,0,0,0,0,0] #The Array element is 6 element in array
	Game_Room_soc.append(Newlist) #append this 6 element in array of bulid 10x6 two axis


def SocketServer(py_tcpCliSockarr):
	global UserRecv,Game_Room_soc
	Username="" #使用者帳號
	UserPass="" #使用者密碼
	while True:
		try:
			UserRecv=py_tcpCliSockarr.recv(BUFSIZ) #接收資訊
		except :
			try:
				print Game_Room_soc[Room_Num]
				socket_name=str(py_tcpCliSockarr)
				for i in range(6):
					Game_Room_soc[Room_Num][i]=0
				print Game_Room_soc[Room_Num]
				print "The room master is disconnect!!!"
			except:
				print Game_Room_soc[int(RoomCode)]
				socket_name=str(py_tcpCliSockarr)
				Game_Room_soc[int(RoomCode)][Append_pos]=0
				print Game_Room_soc[int(RoomCode)]
				print "Is user Leaf the room"
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
					Room_NumMsg="RoomNum"+Room_Num
					py_tcpCliSockarr.send(Room_NumMsg) #send room number
					Room_Num=int(Room_Num) #recover to int

					Game_Room_soc[Room_Num][0]=py_tcpCliSockarr
					#Add this Process socket reference to Game room array use

					break
		if UserRecv[0:10]=="Enter_Room": #if server get client send the room code search created room have created?
			RoomCode=UserRecv.replace("Enter_Room","") #Replace this string "Enter_Room" to get real room code
			print "The user enter Room code is : ",RoomCode
			RoomCode=int(RoomCode)
			try:
				RoomList.index(RoomCode) #Search The user Send Room code ,if not found then goto except function
				py_tcpCliSockarr.send("Found this room code")
				Append_pos=Game_Room_soc[RoomCode].index(0) #use index to find in array integer 0
															#because the 0 is in this array mean "none"
															#so find this array "0" can know how can i do this socket reference append position
				Game_Room_soc[RoomCode][Append_pos]=py_tcpCliSockarr
				#Add this Process socket reference to Game room array use

			except:
				py_tcpCliSockarr.send("Not Found this room code.....")
			RoomCode=str(RoomCode)


		if UserRecv[0:13]=="RoomBroadcast": #is Get user broadcast message
			Game_Room_Num=UserRecv.split("|")[1]
			for i in range(6):
				if str(type(Game_Room_soc[int(Game_Room_Num)][i]))=="<class 'socket._socketobject'>":   #Check this list element is Socket object?
					Game_Room_soc[int(Game_Room_Num)][i].send(UserRecv) #if this element is socket object then send message to user
					#pdb.set_trace()
threading.Thread(target=Get_User_Server).start() #使用者管理線程
