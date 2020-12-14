#! /usr/bin/env python3
from aiohttp import web
import sockethandler
from sockethandler import organizer

async def index(request: web.Request):
    """Serve the client-side application."""
    with open('../frontend/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def room(request: web.Request):
    roomid = request.match_info.get('roomid', "Anonymous")
    room = organizer.getRoomById(roomid)
    if not room:
        return web.HTTPFound(location="/?err=roomnotfound")
    with open('../frontend/room.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def newroom(request: web.Request):
    room = organizer.newRoom()
    print("Room created: " + room.id)
    raise web.HTTPFound(location="/room/"+str(room.id))


def main(host, port):
    app = web.Application()
    sockethandler.attach(app)
    app.router.add_static('/static', '../frontend/static')
    app.router.add_static('/app', '../frontend/app')
    app.router.add_get('/', index)
    app.router.add_get('/room/{roomid}', room)
    app.router.add_get('/newroom', newroom)
    web.run_app(app, host=host, port=port)
    

if __name__ == '__main__':
    main(host = "*", port = 80)
    #main(host = "localhost", port = 8080)