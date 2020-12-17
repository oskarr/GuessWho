import random, constants, os
from constants import BASE_PATH

class Character:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.active = True
    
    # Static, alternate constructor
    def fromDict(d: dict):
        # pylint: disable=no-self-argument, unsubscriptable-object
        return Character(d["name"], d["image"]) 

    def __iter__(self):
        """Only to be used for dict conversion"""
        for k, v in {
                "name": self.name,
                "image": self.image,
                "active": self.active,
            }.items():
            yield (k, v)

class Game:
    def __init__(self):
        faces = constants.FACES.copy()
        names = constants.NAMES.copy()
        random.shuffle(faces)
        random.shuffle(names)
        # TODO allow one char to be on both teams.
        characters = [Character(n, f) for n, f in zip(names[:40], faces[:40])]
        self.teams = {
            "A": {
                "characters": characters[:20],
                "self": None,
                "requestingNewGame" : False,
            },
            "B": {
                "characters": characters[20:],
                "self": None,
                "requestingNewGame" : False,
            }
        }
        self.is_custom = False
        self.path = None
    
    def initFromUserUpload(self, roomid):
        # TODO detta är kodupprepning från __init__...
        localpath = "static/UPC/"+roomid+"/"
        path = BASE_PATH + "/frontend/"+ localpath
        if os.path.isdir(path):
            files = os.listdir(path)
            characters = [Character(f.split(".")[0], localpath+f) for f in files]
            random.shuffle(characters)
            split = min(len(characters)//2, 20)
            self.teams = {
                "A": {
                    "characters": characters[:split],
                    "self": None,
                    "requestingNewGame" : False,
                },
                "B": {
                    "characters": characters[split:],
                    "self": None,
                    "requestingNewGame" : False,
                }
            }
            self.is_custom = True
            self.path = path
        else:
            pass
    
    def restart(self):
        # TODO this is a very ugly solution
        if self.is_custom:
            self.initFromUserUpload(self.path.split("/")[-1])
        else:
            self.__init__()
        
    def getCharactersForTeam(self, team) -> dict:
        return self.teams[team]["characters"]

    def getCharactersForOpposingTeam(self, team) -> dict:
        assert team in "AB"
        return self.teams["A" if team == "B" else "B"]["characters"]
    
    def getTeamSelf(self, team) -> dict:
        return self.teams[team]["self"]

    def getTeam(self, team) -> dict:
        return self.teams[team]

    def getOpposingTeam(self, team) -> dict:
        assert team in "AB"
        return self.teams["A" if team == "B" else "B"]

    def setSelfForTeam(self, team, char: Character):
        self.teams[team]["self"] = char