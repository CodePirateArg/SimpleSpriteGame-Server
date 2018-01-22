import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.0.16.44', 10000)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

name = "User:" + input("Enter UserName: ")

try:
    sock.sendall(name.encode())
    # Send data
    data = sock.recv(1024)
    print(sys.stderr, 'received "%s"' % data)

finally:
    print(sys.stderr, 'closing socket')
    sock.close()
