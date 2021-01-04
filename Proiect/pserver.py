"""
Server pentru problema "Ghicește cifrul"

	@author Alin Clincea
"""

import socket
import random
from _thread import *

def get_ip():
	"""
	Află adresa IP cu ruta implicită pe care rulează serverul.
	Sursa: https://stackoverflow.com/a/28950776

		@returns ip
	"""
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		server.connect(('10.255.255.255', 1))
		ip = server.getsockname()[0]
	except Exception:
		ip = '127.0.0.1'
	finally:
		server.close()
	return ip

def client(connection, address):
	"""
	Gestionează conexiunea unui client în timpul jocului.

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
				message = ""

				if attempt_count == 0:
					message = "GHICEȘTE!"
				elif message == "exit" or not data:
					raise()
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
	Validează inputul și returnează răspunsuri ca string.

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

server = socket.socket()
server_ip = get_ip()
host = "0.0.0.0"
port = 8001
thread_count = 0
buffer_size = 2048

try:
	server.bind((host, port))
except socket.error as e:
	print(str(e))
	exit()

server.listen(5)
print(f"Ghicește cifrul [1.02]\nServerul este pornit.\n\
Conexiunile sunt așteptate la adresa: {server_ip}") #:{port}

while True:
	connection, address = server.accept()
	print(f"\nConexiune nouă pentru clientul {address[0]}:{address[1]}")
	start_new_thread(client, (connection, address, ))
	thread_count += 1
	print(f"Thread #{thread_count}")

server.close()