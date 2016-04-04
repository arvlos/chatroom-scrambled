# Created by Artem Losev
# Creation date: 4/1/2016
# Reference and source of inspiration: the tutorial at bogotobogo.com
# The encrypted client code for the chat application

import sys, socket, select
import encryption

KEY = "Sixteen byte key"


RECV_BUFFER = 4096

def chat_client():
	if len(sys.argv) < 3:
		print "Usage: python client.py hostname port"
		sys.exit()


	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
     
  # connect to remote host
	try:
		s.connect((host, port))
	except:
		print "Unable to connect"
		sys.exit()

	print "Connected to remote host"
	sys.stdout.write("Enter your nickname: "); sys.stdout.flush()
	nickname = sys.stdin.readline()
	nickname = nickname[:-1]
	
	# Send the encrypted version
	s.send(nickname)
	sys.stdout.write("Welcome to our chatroom, %s. You can start sending messages\n" % nickname)
	print_chat_peripherals()

	while True:
		socket_list = [sys.stdin, s]

		# Get the list of readable sockets
		ready_to_read, ready_to_write, error_sockets = select.select(socket_list, [], [])

		for sock in ready_to_read:
			if sock == s:
				# Incoming message from the server 
				data = sock.recv(RECV_BUFFER)

				if not data:
					print "\n Disconnected from chat server\n"
					sys.exit()
				
				else:
					# Print the received data
					sys.stdout.write(data)
					print_chat_peripherals()
			
			else:
				# User entered a message
				msg = sys.stdin.readline()

				# Encryption should happen here before sending
				s.send(msg)
				print_chat_peripherals()


def print_chat_peripherals():
	sys.stdout.write('[Me]: ')
	sys.stdout.flush()


if __name__ == "__main__":
	sys.exit(chat_client())
