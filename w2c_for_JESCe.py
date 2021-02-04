path = "txt/JESC_char/English/test.nm"
out_path = "txt/JESC_char/English/test.nm"

with open(path, encoding="utf-8") as f:
  lines = f.readlines()

out_lines = []
for l in lines:
  print(l)
  l = l.strip()
  l = l.replace(" ", "$")
  out_lines.append((" ".join(list(l))).replace("$", "<sep>"))

with open(out_path, "w", encoding="utf-8") as f:
  f.write("\n".join(out_lines))
