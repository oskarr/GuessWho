import gzip

FACES = ["static/NVSG/"+str(i)+".jpg" for i in range(74074001, 74075000, 2)]

with gzip.open("names.gz", "r") as f:
    NAMES = f.read().decode('utf8').strip().split("\n")