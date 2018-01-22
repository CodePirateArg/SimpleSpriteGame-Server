import sys
import socket


class ServerListener:

    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        print(sys.stderr, "starting on IP: %s Port: %s" % self.server_address)
        self.sock.bind(self.server_address)
        self.users = {}
        self.connections = {}

    def start_listening(self):
        self.sock.listen(1)
        while True:
            print("Waiting for a connection")
            self.connection, self.client_address = self.sock.accept()
            try:
                print(sys.stderr, 'connection from', self.client_address)
                # Receive the data (either a username or a direction)
                while True:
                    data = self.connection.recv(1024)
                    print(sys.stderr, 'received "%s"' % data)
                    decoded_data = data.decode('ascii')
                    if decoded_data[:5] == "User:":
                        temp_username = decoded_data[5:]
                        self.users[temp_username] = [0, 0]
                        print("User: %s has been added to the game" % temp_username)
                        self.connection.sendall(("Welcome %s" % temp_username).encode())
                    else:
                        #print(sys.stderr, 'no more data from', self.client_address)
                        break

            finally:
                # Clean up the connection
                self.connection.close()

    #def register_user(self, username):


def main():
    server = ServerListener('', 10000)
    server.start_listening()


if __name__ == "__main__":
    main()




