#! /usr/bin/env python3

from aiohttp import web
import socketio

## Init
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit('reply', "test", room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    


async def index(request):
    """Serve the client-side application."""
    with open('../frontend/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

app.router.add_static('/static', '../frontend/static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)