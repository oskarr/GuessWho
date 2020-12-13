
class Room:
    """The main game simulation"""

    def __init__(self, id: str):
        self.id = id
        self.participants = []
        self.chat = []
    
    def addParticipant(self, pid: str):
        self.participants.append(pid)
    
    def getParticipants(self):
        return self.participants
    
    def disconnectParticipant(self, pid: str) -> bool:
        return self.participants.remove(pid)