import gzip

FACES = ["static/NVSG/"+str(i)+".jpg" for i in range(74074001, 74075000, 2)]

with gzip.open("names.gz") as f:
    NAMES = f.readlines()