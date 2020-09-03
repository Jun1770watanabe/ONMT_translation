def ngram(n, word):
    if n >= len(word):
        return [word]

    chars = [i for i in word]
    print(chars)
    ng_list = []
    for i in range(len(chars)-n+1):
        ng = chars[i]
        ti = i
        for j in range(n-1):
            ti += 1
            ng += chars[ti]
        ng_list.append(ng)
    return ng_list


input_word = "watanabe"
conf_word = "watamavw"

def comp_ngram(input_word, conf_word, n_max):
    if len(input_word) != len(conf_word):
        print(">> length of word does not match.")
        print(input_word)
        print(conf_word)
        exit()

    for n in range(n_max):
        a = ngram(n+1, input_word)
        b = ngram(n+1, conf_word)

        print(a)
        print(b)
        score = 0
        for i in range(len(a)):
            if a[i] == b[i]:
                score += 1
        score /= len(a)
        print(score)
        if n == 0:
            final_score = score
        else:
            final_score = (final_score + score) / 2  
    print(final_score)

comp_ngram(input_word, conf_word, 4)
exit()