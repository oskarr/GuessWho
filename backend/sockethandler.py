import socketio, html, json

from organizer import Organizer

organizer = Organizer()

sio = socketio.AsyncServer()

@sio.event
def connect(sid, environ):
    print("Connected: ", sid)

@sio.event
async def disconnect(sid):
    print('Disconnected: ', sid)
    await organizer.disconnect(sid)

@sio.event
def update_user(sid, uname, team):
    # TODO disallow updating of team
    print('Update user: ', sid)
    organizer.updateUser(sid, uname, team)

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

@sio.event
async def get_characters(sid):
    room = organizer.getRoomByUserId(sid)
    user = organizer.getUserById(sid)
    print("get_characters from: ",sid)
    if user.team is not None:
        faces = list(map(dict, room.game.getCharactersForTeam(user.team)))
        own = dict(room.game.getTeamSelf(user.team))
        await sio.emit('characters', {"all": faces, "self": own}, room=sid)

@sio.event
async def update_characters(sid, data):
    room = organizer.getRoomByUserId(sid)
    user = organizer.getUserById(sid)
    print("update_characters from: ",sid)
    if user.team is not None:
        team = room.game.teams[user.team]
        # TODO Crazy inefficient.
        # TODO move to the Game class.
        for newchar in data:
            for char in team["characters"]:
                if newchar["name"] == char.name:
                    char.active = newchar["active"]
            
        # = data
        faces = list(map(dict, room.game.getCharactersForTeam(user.team)))
        own = dict(room.game.getTeamSelf(user.team))
        users = organizer.getUsersByRoomId(room.id)
        for u in users:
            if u.id != sid and u.team == user.team:
                print("characters emission to",u.id)
                await sio.emit('characters', {"all": faces, "self": own}, room=u.id)

        

def attach(app):
    sio.attach(app)