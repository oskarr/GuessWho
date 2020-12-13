import socketio

from organizer import Organizer


organizer = Organizer()

sio = socketio.AsyncServer()

@sio.event
def connect(sid, environ):
    print("Connected: ", sid)

@sio.event
def disconnect(sid):
    print('Disconnected: ', sid)

@sio.event
def username(sid, uname):
    organizer.updateUser(sid, uname)

@sio.event
def joinroom(sid, roomid):
    organizer.moveUser(sid, roomid)

@sio.event
async def chat_message(sid, data):
    print("Message from ", sid, ":", data)
    room = organizer.getRoomByUserId(sid)
    users = organizer.getUsersByRoomId(room.id)
    # TODO parallellize
    for user in users:
        if user.id != sid:
            await sio.emit('reply', {"from": sid, "message": data}, room=user.id)

@sio.event
async def room(sid, data):
    if data.action == "join":
        room = organizer.getRoomById(data.roomid)
        if room:
            room.addParticipant(sid)
            print(sid, " joined room ", data.roomid)
            await sio.emit('room', {"action": "confirmation", "success": True}, room=sid)
        else:
            await sio.emit('room', {"action": "confirmation", "success": False}, room=sid)
    elif data.action == "new":
        room = organizer.newRoom()
        await sio.emit('room', {"action": "roomcreated", "roomid": room.id}, room=sid)

def attach(app):
    sio.attach(app)