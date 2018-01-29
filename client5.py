import asyncio
import tkinter as tk
import socket


username = ''


async def tcp_echo_client(loop):
    global username
    reader, writer = await asyncio.open_connection('184.59.100.65', 1001, loop=loop)
    message = input("Enter Message: ")
    print('Send: %r' % message)
    writer.write(message.encode())
    data = await reader.read(100)
    username = data.decode() + ':'
    print('Received: %r' % username)
    writer.close()


def key(event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('184.59.100.65', 1001)
    sock.connect(server_address)
    if event.keysym == 'Escape':
        root.destroy()
        sock.sendall(username.encode() + 'DONE'.encode())
    elif event.char == event.keysym:
        # normal number and letter characters
        sock.sendall(username.encode() + event.char.encode())
    elif len(event.char) == 1:
        # characters like []/.,><#$ also Return and ctrl/key
        sock.sendall(username.encode() + event.char.encode())
    else:
        # f1 to f12, shift keys, caps lock, Home, End, Delete ...
        sock.sendall(username.encode() + event.keysym.encode())
    data = sock.recv(1024)
    print(str(data))
    sock.close()


loop = asyncio.get_event_loop()
i = 0
loop.run_until_complete(tcp_echo_client(loop))
root = tk.Tk()
print("Press a key (Escape key to exit):")
root.bind_all('<Key>', key)
# don't show the tk window
root.mainloop()
loop.close()
