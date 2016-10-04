# -*- coding: utf-8 -*-
import socket
import struct
import hashlib
import FacebookLogin 
from urllib import urlretrieve
HOST = '127.0.0.1'
PORT = 1307
BUFFER_SIZE = 1024
def recv_file():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.bind(server_address)
    print "Starting server on %s port %s" % server_address
    sock.listen(1)
    print u"等待使用者"
    client_socket, client_address = sock.accept()
    fw = open("file_name123123123.mp4", 'wb')
    recv_size = 0
    print u"接收檔案"
    while True :
        file_data = client_socket.recv(BUFFER_SIZE)
        fw.write(file_data)
        if not file_data: break
    fw.close()
    print u"傳輸完畢"

if __name__ == '__main__':
    FacebookLogin.facebook_login()  #先登入facebook 並獲取圖片
    recv_file()