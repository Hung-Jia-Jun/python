import socket

HOST = '127.0.0.1'
PORT = 8812

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
while True:
	clientMessage = input("Command :")
	client.sendall(clientMessage.encode())
	serverMessage = str(client.recv(1024), encoding='utf-8')
	print('Server:', serverMessage)
client.close()