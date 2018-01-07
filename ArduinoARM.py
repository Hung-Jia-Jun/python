import serial
import pdb
from socket import *

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

USBPORT="COM3"
ser =serial.Serial(str(USBPORT),57600) #開啟USBPort

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
	print ('waiting for connection...')
	tcpCliSock,addr = tcpSerSock.accept()
	print ('...connected from: ',addr)
	while True:
		line = ser.readline()  
		message=str(line).split("'")[1].split("\\r")[0]
		print (message)
		tcpCliSock.send(line)
tcpSerSock.close()
ser.close()


