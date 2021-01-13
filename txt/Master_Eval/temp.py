with open("all_char_ans.nm", encoding="utf-8") as f:
    lines = f.readlines()
output = []
for line in lines:
    line = " ".join(list(line))
    output.append(line)
with open("all_char_ans.nm", "w", encoding="utf-8") as f:
    f.write("".join(output))
exit()