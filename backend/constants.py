import gzip, os, pathlib, sys

BASE_PATH = str(pathlib.Path(sys.argv[0]).resolve().parent.parent)

FACES = ["static/NVSG/"+str(i)+".jpg" for i in range(74074001, 74075000, 2)]


with gzip.open(BASE_PATH + "/backend/names.gz", "r") as f:
    NAMES = f.read().decode('utf8').strip().split("\n")
