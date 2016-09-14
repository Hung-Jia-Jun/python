# -*- coding: utf-8 -*-
import os
from socket import *
import SocketServer

BUFSIZ = 2048
def RunSocketServer():
	#python (發送端)
	py_tcpSerSock = socket(AF_INET, SOCK_STREAM)
	py_tcpSerSock.bind(('',31500))
	py_tcpSerSock.listen(50)
	Username=""
	UserPass=""
	while True:
		print u"等待python客戶端連線...port 31500"
		py_tcpCliSock,addr = py_tcpSerSock.accept()  #連接成功後將連線參考物件推入陣列[0]
		print u"python客戶端連線成功"
		while True:
			UserRecv=py_tcpCliSock.recv(BUFSIZ)
			if UserRecv[0:23]=="Login_Facebook_Username":
				UserRecv=UserRecv.replace("Login_Facebook_Username","")
				Username=UserRecv
			if UserRecv[0:23]=="Login_Facebook_Password":
				UserRecv=UserRecv.replace("Login_Facebook_Password","")
				UserPass=UserRecv
			if UserRecv=="Login_Facebook":
				print "Username: ",Username
				print "UserPass: ",UserPass
RunSocketServer()
