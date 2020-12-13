import socketio, aiohttp

class SocketHandler(socketio.AsyncServer):
    def __init__(self, app: aiohttp.web):
        super()
        self.attatch(app)
    @self.event
    def connect(sid, environ):
        print("connect ", sid)

    @self.event
    async def chat_message(sid, data):
        print("message ", data)
        await sio.emit('reply', room=sid)

    @self.event
    def disconnect(sid):
        print('disconnect ', sid)