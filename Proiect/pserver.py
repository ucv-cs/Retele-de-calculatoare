"""
Server pentru problema "Ghicește cifrul"

	@author Alin Clincea
"""

import socket
import random
from _thread import *

server = socket.socket()
host = "0.0.0.0"
port = 8001
thread_count = 0
buffer_size = 2048

try:
	server.bind((host, port))
except socket.error as e:
	print(str(e))

server.listen(5)
print("Serverul este pornit.")

def client(connection, address):
	"""
	Gestionează conexiunea unui client în timpul jocului

		@param connection
		@param address
	"""
	attempt_count = 0
	cipher = random.randint(1, 100)
	started = False

	try:
		while True:
			data = connection.recv(buffer_size)
			print(f"{address[0]}:{address[1]}: {data.decode()}")

			if data.decode() == "START" or started:
				started = True

				if attempt_count == 0:
					message = "GHICEȘTE!"
				elif message == "exit" or not data:
					raise
				else:
					message = test(data.decode(), cipher, attempt_count)

				attempt_count += 1
				connection.sendall(message.encode())
			else:
				connection.sendall("Trebuie să scrii START pentru ca jocul să înceapă.".encode())
	except:
		print(f"Clientul {address[0]}:{address[1]} este deconectat.")
	finally:
		connection.close()

def test(input, cipher, attempt_count):
	"""
	Validează inputul și returnează răspunsuri ca string

		@param input
		@param cipher
		@param attempt_count
		@returns string
	"""
	if input == "exit":
		return "exit"
	try:
		answer = int(input)
		if answer < cipher:
			return "PREA MIC! ÎNCEARCĂ DIN NOU"
		elif answer > cipher:
			return "PREA MARE! ÎNCEARCĂ DIN NOU"
		else:
			return f"AI GHICIT din {attempt_count} încercări!"
	except:
		return "Trebuie să scrii un întreg cuprins între 1 și 100."

while True:
	connection, address = server.accept()
	print(f"\nConexiune nouă pentru clientul {address[0]}:{address[1]}")
	start_new_thread(client, (connection, address, ))
	thread_count += 1
	print(f"Thread #{thread_count}")

server.close()