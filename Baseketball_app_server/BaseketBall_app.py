# -*- coding: utf-8 -*-
from socket import *
import multiprocessing,pdb,sys,os,threading
from msvcrt import getch
User_Sound=""
BUFSIZ = 2048
os.system("chcp 950")  #設定字碼頁
def RunThread():

	SocketTo="localhost"  #遠端server  要改
	PORT = 31500 #轉送python Client端的port
	ADDR = (SocketTo,PORT)
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)


	Username=""
	UserPass=""
	print "Username: "
	Username=raw_input()

	print "UserPass: "
	UserPass=raw_input()
	while True:
		#Recv_Server_Message=tcpCliSock.recv(BUFSIZ) #接收server指令
		SendName="Login_Facebook_Username"+Username
		SendPass="Login_Facebook_Password"+UserPass
		tcpCliSock.send(SendName)
		tcpCliSock.send(SendPass)
		tcpCliSock.send("Login_Facebook")
		raw_input()

if __name__ == '__main__':  #如果執行的是本體的話，才執行下面的語句
	print u"[遠端連線的主機] : "
	#SocketTo="localhost"
	#SocketTo=raw_input()
	#SocketTo="localhost"

	#threading.Thread(target=RunThread).start()

	RunThread()
	#Run_SocketServer()
