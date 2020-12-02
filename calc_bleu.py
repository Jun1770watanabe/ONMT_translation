from nltk.translate.bleu_score import sentence_bleu
import argparse

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument("-re", '--reference', type=str, default='summaries.txt', help='Reference File')
    Argparser.add_argument("-ca", '--candidate', type=str, default='candidates.txt', help='Candidate file')

    args = Argparser.parse_args()
    return args

args = argparser()

with open(args.reference, encoding="utf-8") as f:
    reference = f.readlines()
with open(args.candidate, encoding="utf-8") as f:
    candidate = f.readlines()

if len(reference) != len(candidate):
    raise ValueError('The number of sentences in both files do not match.')

score = 0.

max_ngram = 18
weights = [1./max_ngram for i in range(max_ngram)]

for i in range(len(reference)):
    reference[i] = reference[i].replace(" ", "")
    # score += sentence_bleu([reference[i].strip()], candidate[i].strip())
    score += sentence_bleu([reference[i].strip()], candidate[i].strip(), weights)

score /= len(reference)
print("The bleu score is: "+str(score))