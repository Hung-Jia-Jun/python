# -*- coding: utf-8 -*-
from socket import *
import SocketServer
from msvcrt import getch

import multiprocessing,os,sys,pdb,time,os,threading
BUFSIZ = 2048  #socket 傳輸單檔大小

py_tcpCliSockarr=[] #User的socket參考陣列
def Get_User_Server():  #管理使用者連接伺服器的陣列
	py_tcpSerSock = socket(AF_INET, SOCK_STREAM)
	py_tcpSerSock.bind(('',31500))
	py_tcpSerSock.listen(50)
	while True:
		print u"等待python客戶端連線...port 31500"
		py_tcpCliSock,addr = py_tcpSerSock.accept()  #連接成功後將連線參考物件推入陣列[0]
		py_tcpCliSockarr.append(py_tcpCliSock)
		print py_tcpCliSock
		Cli_Socket_num=len(py_tcpCliSockarr)
		print u"python客戶端連線成功"
		threading.Thread(target=SocketServer,args=(py_tcpCliSockarr,)).start() #使用者回應線程

def SocketServer(py_tcpCliSockarr):
	Username="" #使用者帳號
	UserPass="" #使用者密碼
	while True:
		UserRecv=py_tcpCliSockarr.recv(BUFSIZ) #接收資訊
		if UserRecv[0:23]=="Login_Facebook_Username":  #如果訊息表頭是Login，就將變數存進使用者帳號
			UserRecv=UserRecv.replace("Login_Facebook_Username","")
			Username=UserRecv
		if UserRecv[0:23]=="Login_Facebook_Password":  #如果訊息表頭是PassWord，就將變數存進使用者密碼
			UserRecv=UserRecv.replace("Login_Facebook_Password","")
			UserPass=UserRecv
		if UserRecv=="Login_Facebook":
			print "Username: ",Username
			print "UserPass: ",UserPass

		#if UserRecv==""


threading.Thread(target=Get_User_Server).start() #使用者管理線程

