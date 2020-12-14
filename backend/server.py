#! /usr/bin/env python3
from aiohttp import web
import sockethandler, os, sys, pathlib
from sockethandler import organizer
from constants import BASE_PATH

async def index(request: web.Request):
    """Serve the client-side application."""
    print("[INFO] Serving index.html")
    with open(BASE_PATH + '/frontend/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def room(request: web.Request):
    roomid = request.match_info.get('roomid', "")
    room = organizer.getRoomById(roomid)
    print("[INFO] Serving room ", roomid)
    if not room:
        return web.HTTPFound(location="/?err=roomnotfound")
    with open(BASE_PATH + '/frontend/room.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def newroom(request: web.Request):
    room = organizer.newRoom()
    print("[INFO] Room created: " + room.id)
    raise web.HTTPFound(location="/room/"+str(room.id))


def main():
    print("[INFO] BASE_PATH =", BASE_PATH)
    app = web.Application()
    sockethandler.attach(app)

    app.router.add_static('/static', BASE_PATH + '/frontend/static')
    app.router.add_static('/app', BASE_PATH + '/frontend/app')

    app.router.add_get('/', index)
    app.router.add_get('/room/{roomid}', room)
    app.router.add_get('/newroom', newroom)

    print("[INFO] Attempting to assign server to port ", os.getenv('PORT'))
    web.run_app(app, port = os.getenv('PORT'))
    

if __name__ == '__main__':
    main()