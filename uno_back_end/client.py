import socket
import os
import json
from _thread import start_new_thread

client = socket.socket()
client.connect(('127.0.0.1', 8443))

message_to_send = {
	'username': None,
	'action': None
}

def recv_thread(embo):
	while True:
		data = client.recv(2048)
		data = data.decode('utf-8')
		data = json.loads(data)
		os.system('cls')
		print(json.dumps(data, indent=4))

start_new_thread(recv_thread, (1,))

user_input = input('Enter your username: ')
client.send(user_input.encode('utf-8'))
username = user_input

while True:
	user_input = input()
	message_to_send['username'] = username
	message_to_send['action'] = user_input
	client.send((json.dumps(message_to_send)).encode('utf-8'))