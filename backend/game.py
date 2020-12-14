import random, constants, os
from constants import BASE_PATH

class Character:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.active = True
    
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
        # TODO make own face pickable by user
        characters = [Character(n, f) for n, f in zip(names[:40], faces[:40])]
        self.teams = {
            "A": {
                "characters": characters[:20],
                "self": random.choice(characters[20:]),
            },
            "B": {
                "characters": characters[20:],
                "self": random.choice(characters[:20]),
            }
        }
    
    def initFromUserUpload(self, roomid):
        localpath = "static/user/"+roomid+"/"
        path = BASE_PATH + "/frontend/"+ localpath
        if os.path.isdir(path):
            files = os.listdir(path)
            characters = [Character(f.split(".")[0], localpath+f) for f in files]
            random.shuffle(characters)
            split = min(len(characters)//2, 20)
            self.teams = {
                "A": {
                    "characters": characters[:split],
                    "self": random.choice(characters[split:]),
                },
                "B": {
                    "characters": characters[split:],
                    "self": random.choice(characters[:split]),
                }
            }
        else:
            pass

    def getCharactersForTeam(self, team) -> dict:
        return self.teams[team]["characters"]
    
    def getTeamSelf(self, team) -> dict:
        return self.teams[team]["self"]
