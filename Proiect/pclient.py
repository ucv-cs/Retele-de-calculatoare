"""
Client pentru problema "Ghicește cifrul"

	@author Alin Clincea
"""

import socket

print("Ghicește cifrul [1.02]\nClientul este pornit.\n")
client = socket.socket()
server = input("Scrie adresa serverului: ")
port = 8001
buffer_size = 2048

try:
	client.connect((server, port))
except socket.error as e:
	print(str(e))
	exit()

message = input("Scrie START pentru a începe: ")

while message != "exit":
	client.sendall(message.encode())
	data = client.recv(buffer_size)
	print(f"Server: {data.decode()}")

	if "GHICIT" in data.decode():
		client.sendall("exit".encode())
		break

	message = input("Scrie răspunsul: ")

client.sendall("exit".encode())

client.close()