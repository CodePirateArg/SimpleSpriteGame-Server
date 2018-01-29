import asyncio


users = []


class Player:
    username = ''
    x = 0
    y = 0
    message = ''
    coordinates = ''.encode()
    def moveright(self):
        self.x += 1
    def moveleft(self):
        self.x -= 1
    def moveup(self):
        self.y += 1
    def movedown(self):
        self.y -= 1
    def set_coordinates(self):
        if self.message == 'Left':
            self.moveleft()
            self.coordinates = ('(' + str(self.x) + ',' + str(self.y) + ')').encode()
        elif self.message == 'Right':
            self.moveright()
            self.coordinates = ('(' + str(self.x) + ',' + str(self.y) + ')').encode()
        elif self.message == 'Up':
            self.moveup()
            self.coordinates = ('(' + str(self.x) + ',' + str(self.y) + ')').encode()
        elif self.message == 'Down':
            self.movedown()
            self.coordinates = ('(' + str(self.x) + ',' + str(self.y) + ')').encode()


async def handle_echo(reader, writer):
    global users
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    if ':' not in message:
        writer.write(data)
        player = Player()
        player.username = data.decode()
        users.append(player)
    else:
        username = message.split(':', 1)[0]
        for user in users:
            if user.username == username:
                user.message = message.split(':', 1)[1]
                user.set_coordinates()
                writer.write(user.coordinates)
    await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '192.168.0.11', 1000, loop=loop)
server = loop.run_until_complete(coro)
# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()