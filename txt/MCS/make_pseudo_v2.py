import random

def ins_miss(char):
    # print(">> ins")
    return char *2

def sub_miss(char):
    # print(">> trs")
    if char == "0":
        return "9" 
    elif char == "1":
        return "2" 
    elif char == "2":
        return "3"
    elif char == "3":
        return "2" 
    elif char == "4":
        return "7" 
    elif char == "7":
        return "4" 
    elif char == "8":
        return "9" 
    elif char == "9":
        return "8" 


text_path = "../wmt17/test.nm"
with open(text_path, encoding="utf-8") as f:
    lines = f.readlines()

new_text = []
cnt = 0
for l in lines:
    text_l = []
    l = l.replace("\n", "")
    # print(l)
    for c in list(l):
        sw = random.random()
        if c == " ":
            text_l.append(c)
            continue

        if sw < 0.00393: # delete
            print("delete")
            continue
        elif sw < 0.00269:
            print("insert")
            text_l.append(ins_miss(c))
            continue
        elif sw < 0.00786:
            print("substitution")
            text_l.append(sub_miss(c))
            continue
        text_l.append(c)
    # print("".join(text_l))
    cnt += 1
    print(cnt)
    # print(text_l)
    new_text.append("".join(text_l))
new_text = "\n".join(new_text)

text_path = "test_output.nm"
with open(text_path, 'w', encoding="utf-8") as f:
    f.write(new_text)
