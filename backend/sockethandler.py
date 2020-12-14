import socketio, html

from organizer import Organizer

organizer = Organizer()

sio = socketio.AsyncServer()

@sio.event
def connect(sid, environ):
    print("Connected: ", sid)

@sio.event
def disconnect(sid):
    print('Disconnected: ', sid)
    organizer.disconnect(sid)

@sio.event
def username(sid, uname):
    organizer.updateUser(sid, uname)

@sio.event
async def joinroom(sid, roomid):
    room = organizer.getRoomById(roomid)
    if room:
        organizer.moveUser(sid, roomid)
        print(sid, " joined room ", roomid)
        await sio.emit('room', {"action": "confirmation", "success": True}, room=sid)
        for message in room.chat:
            await sio.emit('reply', {"from": message.sender, "message": message.message}, room=sid)
    else:
        await sio.emit('room', {"action": "confirmation", "success": False}, room=sid)

@sio.event
async def chat_message(sid, data):
    data = html.escape(data)
    print("Message from ", sid, ":", data)
    room = organizer.getRoomByUserId(sid)
    users = organizer.getUsersByRoomId(room.id)
    room.addMessage(sid, data)

    # TODO parallellize
    for user in users:
        if user.id != sid:
            await sio.emit('reply', {"from": sid, "message": data}, room=user.id)
            

def attach(app):
    sio.attach(app)