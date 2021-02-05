path = "../210108_Yahoo_word_trsf_step_52000_jesc_char.jp"

with open(path, encoding="utf-8") as f:
    lines = f.readlines()

out_list = []
for l in lines:
    l = l.replace("<unk>", "&")
    l = l.replace(" ", "")
    l = " ".join(list(l))
    l = l.replace("&", "<unk>")
    out_list.append(l)

with open(path, "w", encoding="utf-8") as f:
    f.write("".join(out_list))
