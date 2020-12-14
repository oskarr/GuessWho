import gzip, os

FACES = ["static/NVSG/"+str(i)+".jpg" for i in range(74074001, 74075000, 2)]


if os.path.isfile('names.gz'):
    with gzip.open("names.gz", "r") as f:
        NAMES = f.read().decode('utf8').strip().split("\n")
elif os.path.isfile('backend/names.gz'): # Heroku needs this
    with gzip.open("backend/names.gz", "r") as f:
            NAMES = f.read().decode('utf8').strip().split("\n")
else:
    print("names.gz not found. Current directory contents: ", os.listdir())
    raise FileNotFoundError
