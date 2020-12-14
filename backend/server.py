#! /usr/bin/env python3
from aiohttp import web
import sockethandler, os, sys, pathlib
from sockethandler import organizer
from constants import BASE_PATH

async def index(request: web.Request):
    """Serve the client-side application."""
    with open(sys.argv[0] + '/../frontend/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def room(request: web.Request):
    roomid = request.match_info.get('roomid', "Anonymous")
    room = organizer.getRoomById(roomid)
    if not room:
        return web.HTTPFound(location="/?err=roomnotfound")
    with open(sys.argv[0] + '/../frontend/room.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def newroom(request: web.Request):
    room = organizer.newRoom()
    print("Room created: " + room.id)
    raise web.HTTPFound(location="/room/"+str(room.id))


def main(host, port):
    print("[INFO] BASE_PATH =", BASE_PATH)
    app = web.Application()
    sockethandler.attach(app)

    app.router.add_static('/static', BASE_PATH + '/frontend/static')
    app.router.add_static('/app', BASE_PATH + '/frontend/app')

    app.router.add_get('/', index)
    app.router.add_get('/room/{roomid}', room)
    app.router.add_get('/newroom', newroom)
    web.run_app(app, host=host, port=port)
    

if __name__ == '__main__':
    #main(host = "localhost", port = os.getenv('PORT'))
    main(host = "localhost", port = 8080)