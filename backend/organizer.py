"""Contains code for organizing users into rooms."""

import string, random

class Room:
    """Contains the info for a room."""
    def __init__(self, rid: str):
        self.id = rid
        self.participants = []
        self.chat = []


class User:
    """Contains a user and its id."""
    def __init__(self, uid, name):
        self.id = uid
        self.name = name


class Organizer:
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
    
    def updateUser(self, sid: str, uname: str):
        user = self.getUserById(sid)
        if user:
            user.name = uname
        else:
            self.users.append(User(sid, uname))
    
    def moveUser(self, sid: str, roomid: str):
        if self.getUserById(sid) and self.getRoomById(roomid):
            self.map[sid] = roomid
        else:
            assert False
    
    def disconnect(self, sid):
        try:
            roomid = self.map[sid]
            # Delete empty rooms
            # TODO make this a delay, so that reloading won't delete the room.
            if len(self.getUsersByRoomId(roomid)) == 1:
                for idx, room in enumerate(self.rooms):
                    if room.id == roomid:
                        del self.rooms[idx]
                        print("Deleted empty room: "+str(roomid))
                        break

            del self.map[sid]
        except:
            print("WARNING: Failed to remove sid {} from backend. Were they ever connected?".format(sid))

    # TODO, either cache these, or make it a binary search
    def getUserById(self, uid: str):
        for user in self.users:
            if user.id == uid:
                return user
        return False
    
    def getUserByName(self, uname: str):
        for user in self.users:
            if user.name == uname:
                return user
        return False
    
    def getRoomById(self, roomId: str):
        for room in self.rooms:
            if room.id == roomId:
                return room
        return False
    
    def getRoomByUserId(self, uid: str):
        return self.getRoomById(self.map[uid])
    
    def getUsersByRoomId(self, roomid: str):
        roomusers = [uid for uid, rid in self.map.items() if rid == roomid]
        return [user for user in self.users if user.id in roomusers]