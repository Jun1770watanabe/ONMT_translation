with open(opt.tgt, encoding="utf-8") as f:
    text = f.readlines()

acc = []
n_max = 50
dist = np.zeros((n_max))
correct_cnt = len(pred_sents)
for i in range(len(pred_sents)):
    pre = pred_sents[i][0].split()
    ans = text[i].split()
    if len(ans) >= n_max:
        continue
    if len(pre) != len(ans):
        print(pre)
        print(ans)
        print(">> length of sentences does not match.")
        continue

    n = len(pre)
    cnt = 0
    for j in range(n):
        if pre[j] == ans[j]:
            cnt += 1

    # if sentences didn't match, display both.
    if cnt / n < 1:
        correct_cnt -= 1
        print(">> No." + str(i) + " sentences didn't match !")
        print(">> estimated: " + pred_sents[i][0])
        print(">> answer:    " + text[i])
    
    acc.append((i, n, cnt / n))
    dist[len(ans)] += 1
print(">> correct sentences: " + str(correct_cnt) + "/" + str(len(pred_sents)))

# make acc list from acc tapple
acc_list = [[] for i in range(n_max)]
for i in acc:
    acc_list[i[1]].append(i[2])
acc_list = [sum(i)/len(i) for i in acc_list if len(i) != 0]

idx = [i for i in range(len(dist)) if dist[i] != 0]
ave = sum(acc_list) * 100 / len(acc_list)
print(">> average of accuracy rate: {} %".format(ave))

save_data_as_list(idx, acc_list, list(np.arange(n_max)), list(dist))
exit()


def save_data_as_list(d1, d2, d3, d4):
    d = []
    d.append(d1)
    d.append(d2)
    d.append(d3)
    d.append(d4)

    with open("data_.txt", 'w', encoding="utf-8") as f:
        for i in d:
            f.write(str(i) + "\n")
