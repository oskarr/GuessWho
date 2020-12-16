"""Contains code for organizing users into rooms."""

import string, time, random, asyncio, game, shutil, os
from constants import BASE_PATH

class Message:
    def __init__(self, sid, message):
        self.sender = sid
        self.message = message
        self.time = time.time()


class User:
    """Contains a user and its id."""
    def __init__(self, sid, name, team = None):
        self.id = sid
        self.name = name
        self.team = team


class Room:
    """Contains the info for a room."""
    def __init__(self, rid: str):
        self.id = rid
        self.participants = []
        self.chat = []
        self.lastaccess = None
        self.game = game.Game()
    
    def addMessage(self, sid, message):
        self.chat.append(Message(sid, message))


class Organizer:
    """Effectively works as a database"""
    def __init__(self):
        self.rooms = []
        self.users = []
        # Maps a user to a room
        self.map = {}
    
    def newRoom(self) -> Room:
        "Creates a new room, and returns that room."

        # Generate a new room id. We have 26^16 combinations
        roomId = None
        while roomId is None or self.getRoomById(roomId):
            roomId = ''.join(random.choice(string.ascii_letters) for _ in range(16))

        room = Room(roomId)

        self.rooms.append(room)
        return room
    
    def updateUser(self, sid: str, uname: str, team = None):
        user = self.getUserById(sid)
        if user:
            user.name = uname
            if team is not None:
                user.team = team
        else:
            self.users.append(User(sid, uname, team))
    
    def moveUser(self, sid: str, roomid: str):
        if self.getUserById(sid) and self.getRoomById(roomid):
            self.map[sid] = roomid
        else:
            assert False
    
    def deleteRoom(self, roomid, delay = 3, force = False):
        # TODO make delay work
        #print("Pending deletion of: ", roomid, " in ", delay, "s")
        #await asyncio.sleep(delay)
        #print("Started deletion of: ", roomid)
        for idx, room in enumerate(self.rooms):
                if room.id == roomid:
                    if len(self.getUsersByRoomId(roomid))==0 or force:
                        del self.rooms[idx]

                        roompath = BASE_PATH + "/frontend/static/UPC/"+roomid
                        if os.path.isdir(roompath):
                            shutil.rmtree(roompath)
                        print("Deleted room: "+str(roomid))
                    else:
                        print("Didn't delete room: "+str(roomid)+" room is not empty.")
                    break

    async def disconnect(self, sid):
        try:
            roomid = self.map[sid]
            del self.map[sid]
            # Delete empty rooms
            # TODO make this a delay, so that reloading won't delete the room.
            if len(self.getUsersByRoomId(roomid)) == 0:
                self.deleteRoom(roomid)

        except KeyError:
            print("WARNING: Failed to remove sid {} from backend. Were they ever connected?".format(sid))

    # TODO, either cache these, or make it a binary search
    def getUserById(self, uid: str) -> User:
        for user in self.users:
            if user.id == uid:
                return user
        return False
    
    def getUserByName(self, uname: str) -> User:
        for user in self.users:
            if user.name == uname:
                return user
        return False
    
    def getRoomById(self, roomId: str) -> Room:
        for room in self.rooms:
            if room.id == roomId:
                return room
        return False
    
    def getRoomByUserId(self, uid: str) -> Room:
        return self.getRoomById(self.map[uid])
    
    def getUsersByRoomId(self, roomid: str) -> [User]:
        roomusers = [uid for uid, rid in self.map.items() if rid == roomid]
        return [user for user in self.users if user.id in roomusers]