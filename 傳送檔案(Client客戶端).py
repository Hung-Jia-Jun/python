# -*- coding: utf-8 -*-
import socket
import struct
import os
import time
import hashlib
HOST = 'localhost'
PORT = 1307
BUFFER_SIZE = 2048
FILE_NAME = 'C:\\Users\\PC\\Documents\\oCam\\2016_05_06_02_28_57_121.mp4'   # Change to your file
FILE_SIZE = os.path.getsize(FILE_NAME)

def send_file():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    fr = open(FILE_NAME, 'rb')  #開啟要傳輸的擋案
    sock.connect(server_address)
    send_size = 0
    while True:  #如果未發送數據>已發送數據  就繼續傳送
        file_data = fr.read(BUFFER_SIZE)
        sock.send(file_data)
        if not file_data: break
        print "Send..."
    print "Send success!"
    fr.close()
    sock.close()

if __name__ == '__main__':
    send_file()