import matplotlib.pyplot as plt
import numpy as np
import pickle

# # if plot two accuracy data with distribution

# with open("result/data_dist_rwjj_c.pickle", "rb") as f:
#     d1 = pickle.load(f)
# with open("result/data_dist_twjj_c.pickle", "rb") as f:
#     d2 = pickle.load(f)

# fig = plt.figure(figsize=(14,5))
# ax1 = fig.add_subplot(111)
# ax1.plot(d1[2], d1[3], color="red", marker=".", label="SAR(B)")
# ax1.plot(d2[2], d2[3], color="chocolate", marker=".", label="SAR(T)")
# ax2 = ax1.twinx()
# ax2.plot(d1[0], d1[1], color="blue", marker=".", label="NoS")
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# ax1.legend(h1+h2, l1+l2, loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=18)

# ax1.set_xlabel("Number of Characters", fontsize=20)
# ax1.set_ylabel("SAR", fontsize=20)
# # ax1.xlim()
# ax1.set_ylim(0,100)
# ax1.tick_params(labelsize=18)
# # ax1.xaxis.set_ticks(np.arange(0, 100, 10))
# ax1.grid(True)
# # ax2.ylim()
# ax2.tick_params(labelsize=18)
# ax2.set_ylabel("Number of Sentences", fontsize=20)
# plt.tight_layout()
# # plt.tick_params(labelsize=13)
# plt.show()
# exit()

# if plot four accuracy data with distribution

with open("result/acc_dist_rcjj.pickle", "rb") as f:
    d1 = pickle.load(f)
with open("result/acc_dist_tcjj.pickle", "rb") as f:
    d2 = pickle.load(f)
with open("result/data_dist_rwjj_c.pickle", "rb") as f:
    d3 = pickle.load(f)
with open("result/data_dist_twjj_c.pickle", "rb") as f:
    d4 = pickle.load(f)

fig = plt.figure(figsize=(14,5))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
# ax2.plot(d1[0], d1[1], color="blue", marker=".", label="NoS")
ax2.bar(d1[0], d1[1], color="blue", label="NoS")
ax1.plot(d1[2], d1[3], color="red", marker=".", label="SAR(B)")
ax1.plot(d2[2], d2[3], color="green", marker=".", label="SAR(T)")
ax1.plot(d3[2], d3[3], color="darkorange", marker=".", label="SAR(B)")
ax1.plot(d4[2], d4[3], color="violet", marker=".", label="SAR(T)")
# ax2 = ax1.twinx()
# # ax2.plot(d1[0], d1[1], color="blue", marker=".", label="NoS")
# ax2.bar(d1[0], d1[1], color="blue", label="NoS")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=18)

ax1.set_xlabel("Number of Characters", fontsize=20)
ax1.set_ylabel("SAR", fontsize=20)
# ax1.xlim()
ax1.set_ylim(0,100)
ax1.tick_params(labelsize=18)
# ax1.xaxis.set_ticks(np.arange(0, 100, 10))
ax1.grid(True)
# ax2.ylim()
ax2.tick_params(labelsize=18)
ax2.set_ylabel("Number of Sentences", fontsize=20)
plt.tight_layout()
# plt.tick_params(labelsize=13)
plt.show()
exit()