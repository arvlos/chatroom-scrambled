# Created by Artem Losev
# Creation date: 4/1/2016
# Reference and source of inspiration: the tutorial at bogotobogo.com

import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9000

def chat_server():

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# Add the server socket to the list of readable connections
	SOCKET_LIST.append(server_socket)

	print "Chat server started on port " + str(PORT)

	while True:

		# Get the list of sockets that are ready to be read through Select 
		# Set the timeout arg to 0
		ready_to_read, ready_to_write, error_sockets = select.select(SOCKET_LIST, [], [], 0)

		for sock in ready_to_read:
			# A new connection request received
			if sock == server_socket:
				new_socket, address = server_socket.accept()
				SOCKET_LIST.append(new_socket)
				print "Client (%s, %s) connected" % address

				broadcast(server_socket, new_socket, "[%s:%s] entered our chat room\n" % address)

			# A message from a client, not a new connection
			else:
				# Process data from the client
				try:
					# Receiving data from the socket
					data = sock.recv(RECV_BUFFER)

					if data:
						# Means there is something in the socket
						broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
					
					else:
						# There is nothing to be read, remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % address)

				# Exception
				except:
					broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % address)
					continue

	server_socket.close()


# Broadcast chat messages to all the clients
def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
		# Send the message only to peer
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				# Broken socket connection
				socket.close()

				# Remove broken socket
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)


if __name__ == "__main__":

	sys.exit(chat_server())
