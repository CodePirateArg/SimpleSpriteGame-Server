import sys
import socket
import threading
import asyncio


class ServerListener:

    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        print(sys.stderr, "starting on IP: %s Port: %s" % self.server_address)
        self.sock.bind(self.server_address)
        self.users = {}
        self.connections = {}

    def receive_data(self, connection):
        while True:
            data = connection.recv(1024)
            print(sys.stderr, 'received "%s"' % data)
            decoded_data = data.decode('ascii')
            if decoded_data[:5] == "User:":
                temp_username = decoded_data[5:]
                self.users[temp_username] = [0, 0]
                print("User: %s has been added to the game" % temp_username)
                connection.sendall(("Welcome %s" % temp_username).encode())
            else:
                # print(sys.stderr, 'no more data from', self.client_address)
                break


    def start_listening(self):
        self.sock.listen(1)
        while True:
            print("Waiting for a connection")
            connection, client_address = self.sock.accept()
            print(connection)
            try:
                print(sys.stderr, 'connection from', client_address)
                # Receive the data (either a username or a direction)
                thread = threading.Thread(target=self.receive_data(connection))
                thread.start()

            finally:
                # Clean up the connection
                print("connection closed")
                connection.close()

    #def register_user(self, username):


def main():
    server = ServerListener('', 10000)
    server.start_listening()
    #thread = threading.Thread(target=server.start_listening(), args=())
    #thread2 = threading.Thread(target=server.start_listening(), args=())
    #thread.daemon = True
    #thread2.daemon = True
    #thread.start()
    #thread2.start()
    ##ioloop = asyncio.get_event_loop()
    ##tasks = [ioloop.create_task(server.start_listening())]
    ##wait_tasks = asyncio.wait(tasks)
    ##ioloop.run_until_complete(wait_tasks)
    ##ioloop.close()


if __name__ == "__main__":
    main()




