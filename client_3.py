import asyncio
import tkinter as tk
import socket



async def tcp_echo_client(loop):
    reader, writer = await asyncio.open_connection('192.168.0.11', 1000, loop=loop)
    message = input("Enter Message: ")
    print('Send: %r' % message)
    writer.write(message.encode())
    data = await reader.read(100)
    print('Received: %r' % data.decode())
    writer.close()


def key(event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.11', 1000)
    sock.connect(server_address)
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        # normal number and letter characters
        sock.sendall(event.char.encode())
    elif len(event.char) == 1:
        # characters like []/.,><#$ also Return and ctrl/key
        sock.sendall(event.keysym, event.char.encode())
    else:
        # f1 to f12, shift keys, caps lock, Home, End, Delete ...
        sock.sendall(event.keysym.encode())
    data = sock.recv(1024)
    print(str(data))
    sock.close()


loop = asyncio.get_event_loop()
i = 0
while True:
    loop.run_until_complete(tcp_echo_client(loop))
    root = tk.Tk()
    if i == 0:
        print("Press a key (Escape key to exit):")
        i += 1
    root.bind_all('<Key>', key)
    # don't show the tk window
    root.mainloop()
loop.close()
