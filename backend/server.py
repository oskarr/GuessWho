#! /usr/bin/env python3
from aiohttp import web, MultipartReader
import sockethandler, os, io, sys, pathlib, zipfile, shutil
from sockethandler import organizer
from constants import BASE_PATH

# TODO move directories to constants.

async def index(request: web.Request):
    """Serve the client-side application."""
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

async def newcustomroom(request: web.Request):
    #post = await request.post()
    #print("FILE:", post.get("file"))


    reader = await request.multipart()
    files = {}

    while True:
        part = await reader.next()
        if part is None:
            break
        if part.filename:
            files[part.filename] = await part.read(decode=False)

    if len(files) == 0:
        raise web.HTTPFound(location="/?err=nofileprovided")
    elif len(files) == 1 and list(files.keys())[0][-4:] != ".zip":
        print(list(files.keys()))
        raise web.HTTPFound(location="/?err=notazip")
    

    room = organizer.newRoom()
    print("[INFO] Custom room created: " + room.id)
    #print("Files:", list(files.keys()))

    folder = os.path.join(BASE_PATH+"/frontend/static/UPC/", room.id) + "/"
    os.mkdir(folder)
    overwritten = False

    for fname, data in files.items():
        if fname[-4:] == ".zip":
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for f in z.filelist:
                    fn = f.filename
                    if isImage(fn):
                        if os.path.isfile(folder+fn):
                            overwritten = True
                        with open(folder+fn, "wb") as xf:
                            xf.write(z.read(fn))
        elif isImage(fname):
            if os.path.isfile(folder+fname):
                overwritten = True
            with open(folder+fname, "wb") as f:
                f.write(data)
        else:
            print("File provided of unknown format: ", fname)

    if len(os.listdir(folder)) < 2:
        organizer.deleteRoom(room.id)
        raise web.HTTPFound(location="/?err=toofewfiles")
    else:
        # TODO alert the user of overwritten files, or change the name of those files.
        room.game.initFromUserUpload(room.id)
        raise web.HTTPFound(location="/room/"+str(room.id) + ("?overwritten=1" if overwritten else ""))

def isImage(filename: str) -> bool:
    return filename[-4:].lower() in [".jpg", ".png", ".gif", ".bmp"] \
        or filename[-5:].lower() in [".jpeg", ".jfif", ".tiff", ".webp"]

def main():
    print("[INFO] BASE_PATH =", BASE_PATH)
    app = web.Application()
    sockethandler.attach(app)

    app.router.add_static('/static', BASE_PATH + '/frontend/static')
    app.router.add_static('/app', BASE_PATH + '/frontend/app')

    app.router.add_get('/', index)
    app.router.add_get('/room/{roomid}', room)
    app.router.add_get('/newroom', newroom)
    app.router.add_post('/newcustomroom', newcustomroom)

    print("[INFO] Attempting to assign server to port ", os.getenv('PORT'))
    print("[INFO] Don't forget to manually clean /static/UPC/ if shutting down manually.")
    web.run_app(app, port = os.getenv('PORT'))
    

if __name__ == '__main__':
    main()