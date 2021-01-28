from nltk.translate.bleu_score import sentence_bleu
import argparse

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument("-re", '--reference', type=str, default='summaries.txt', help='Reference File')
    Argparser.add_argument("-hy", '--hypothesis', type=str, default='hypothesis.txt', help='Hypothesis file')

    args = Argparser.parse_args()
    return args

args = argparser()

with open(args.reference, encoding="utf-8") as f:
    reference = f.readlines()
with open(args.hypothesis, encoding="utf-8") as f:
    hypothesis = f.readlines()

print(len(reference))
print(len(hypothesis))
if len(reference) != len(hypothesis):
    raise ValueError('The number of sentences in both files do not match.')

score = 0.

max_ngram = 4
weights = [1./max_ngram for i in range(max_ngram)]

for i in range(len(reference)):
    # # for character
    # reference[i] = reference[i].split(" ")
    # score += sentence_bleu([reference[i].strip()], hypothesis[i].strip(), weights)

    # for word
    score += sentence_bleu([reference[i].split(" ")], hypothesis[i].split(" "), weights)

score /= len(reference)
print("The bleu score is: "+str(score))