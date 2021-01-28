import pickle
import Levenshtein

def Comp_words(word):
    with open("vocab/vocab_jp_nm.pickle", "rb") as f:
        vocab = pickle.load(f)

    Dist = 0
    word_c = ""
    for i in vocab:
        LJW = Levenshtein.jaro_winkler(word, i[0])
        if Dist < LJW:
            Dist = LJW
            word_c = i[0]
    # print(Dist)
    return word_c

str = "21417133"
print(Comp_words(str))

