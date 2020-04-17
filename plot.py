import matplotlib.pyplot as plt
import numpy as np

def read_list(path):
    with open(path, encoding="utf-8") as f:
        list_row = []
        for x in f:
            list_row.append(x.rstrip("\n"))
    return list_row

def prep(data_list):
    for i in range(len(data_list)):
        data_list[i] = data_list[i].replace('[', '')
        data_list[i] = data_list[i].replace(']', '')
        data_list[i] = data_list[i].replace(' ', '')
        data_list[i] = data_list[i].split(',')
        if i == 1:
            data_list[i] = [float(d) for d in data_list[i]]
        elif i == 3:
            data_list[i] = [int(float(d)) for d in data_list[i]]
        else:
            data_list[i] = [int(d) for d in data_list[i]]
    print(data_list)

    return data_list

d1 = read_list("data/data_JESC_jp.txt")
# d1 = read_list("data/data_wmt17_2000_wmt17.txt")
d2 = read_list("data/data_wmt17_280_wmt17.txt")
d3 = read_list("data/data_JESC_en_wmt17.txt")

d1 = prep(d1)
d2 = prep(d2)
d3 = prep(d3)


fig, ax1 = plt.subplots(figsize=(12,8))
ax1.plot(d1[0], d1[1], marker="^", color="red", linewidth=3, label="JESC_jp")
# ax1.plot(d2[0], d2[1], marker="^", color="sienna", linewidth=3, label="wmt17_280")
# ax1.plot(d3[0], d3[1], marker="^", color="orange", linewidth=3, label="JESC_En")
ax2 = ax1.twinx()
ax2.plot(d1[2], d1[3], marker="o", linewidth=3, label="num of sentences")

ax1.set_ylabel("accuracy", fontsize=18)
ax1.set_ylim([0.4, 1.05])
ax2.set_ylim([0, 500])
ax2.set_xlim([0, 50])
ax1.set_xlabel("number of words in a sentence", fontsize=18)
ax2.set_ylabel("number of sentences", fontsize=18)
ax1.tick_params(labelsize=18)
ax2.tick_params(labelsize=18)

handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()
ax1.legend(handler1 + handler2, label1 + label2, bbox_to_anchor=(0.6, 0.48), 
    loc="upper left", fontsize=20)

plt.grid(which="both")

plt.show()
exit()

plt.savefig('acc_dist.png')   