import pickle


f = open("BNF.in", "r", encoding="utf-8")

lines = f.readlines()
result = dict()
count = 0
l = dict()
for line in lines:
    line = line.strip()
    if line == "":
        continue
    token, val = line.split("->")
    token = token.strip()
    l[count] = [token, val]

    val = val.split()
    leng = len(val)
    if val[0] == "''":
        leng = 0
    result[count] = [token, leng]
    count += 1
with open("cfg.pickle", "wb") as f:
    pickle.dump(result, f)
print(result)