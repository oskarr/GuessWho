import gzip, os, pathlib, sys

BASE_PATH = str(pathlib.Path(sys.argv[0]).resolve().parent.parent)

FACES = ["static/NVSG/0"+str(i)+".jpg" for i in range(74001, 75000, 2)]


with gzip.open(BASE_PATH + "/backend/names.gz", "r") as f:
    NAMES = f.read().decode('utf8').strip().split("\n")
