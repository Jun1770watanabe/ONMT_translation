path = "test.jp"

with open(path, encoding="utf-8") as f:
    data = f.readlines()

cnt = 0
for l in data:
    cnt += len(l.split())
print(cnt)
exit()