import socketio, html, json

from organizer import Organizer
from game import Character

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


##
## Broadcast helpers
##
def getCharacterDict(room, team):
    faces = list(map(dict, room.game.getCharactersForTeam(team)))
    opp = list(map(dict, room.game.getCharactersForOpposingTeam(team)))
    own = room.game.getTeamSelf(team)
    own = dict(own) if own is not None else None
    return {"self": own, "all": faces, "opponent": opp}

async def sendCharacters(room, team, sid = None):
    users = organizer.getUsersByRoomId(room.id)
    for u in users:
        if u.id != sid and u.team == team:
            print("characters emission to",u.id)
            await sio.emit('characters', getCharacterDict(room, team), room=u.id)

@sio.event
async def get_characters(sid):
    room = organizer.getRoomByUserId(sid)
    user = organizer.getUserById(sid)
    print("get_characters from: ",sid)
    if user.team is not None:
        await sio.emit('characters', getCharacterDict(room, user.team), room=sid)


@sio.event
async def select_character(sid, character):
    room = organizer.getRoomByUserId(sid)
    user = organizer.getUserById(sid)
    game = room.game
    if user.team is not None:
        for char in game.getCharactersForOpposingTeam(user.team):
            if character["name"] == char.name:
                room.game.setSelfForTeam(user.team, Character.fromDict(character))
        
        await sendCharacters(room, user.team)
    

@sio.event
async def update_characters(sid, data):
    room = organizer.getRoomByUserId(sid)
    user = organizer.getUserById(sid)
    print("update_characters from: ", sid)
    if user.team is not None:
        team = room.game.getTeam(user.team)
        # TODO Crazy inefficient.
        # TODO move to the Game class.
        for newchar in data:
            for char in team["characters"]:
                if newchar["name"] == char.name:
                    char.active = newchar["active"]
            
        # = data
        await sendCharacters(room, user.team, sid)

        

def attach(app):
    sio.attach(app)