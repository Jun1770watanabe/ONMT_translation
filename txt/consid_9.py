import io

with io.open("test.jp", encoding="utf-8") as f:
    ans = f.readlines()
#     ans = f.read()
# ans.replace("\n ", "\n")
# with io.open("test.jp", "w", encoding="utf-8") as f:
#     f.write(ans)
#     exit()


with io.open("pred.jp", encoding="utf-8") as f:
    pre = f.readlines()

for i in range(len(ans)):
    if len(ans[i].split()) == 9:
        print("=========================================")
        print("   answer: {}".format(ans[i]))
        print("predicted: {}".format(pre[i]))
        print("=========================================")
