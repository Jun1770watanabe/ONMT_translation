import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fileA", help="file A", type=str)
parser.add_argument("fileB", help="file B", type=str)
args = parser.parse_args()

with open(args.fileA, encoding="utf-8") as f:
    linesA = f.readlines()
with open(args.fileB, encoding="utf-8") as f:
    linesB = f.readlines()

print(">> comparing {a} and {b} ...".format(a=args.fileA, b=args.fileB))
numl = len(linesA)
assert numl == len(linesB)

ccnt = 0
for n in range(numl):
    linesA[n] = linesA[n].replace("\n", "")
    linesB[n] = linesB[n].replace("\n", "")
    if linesA[n] == linesB[n]:
        ccnt += 1
        continue
    else:
        print("== Line " + str(n+1) + " ==")
        print("***** " + args.fileA)
        print(linesA[n])
        print("***** " + args.fileB)
        print(linesB[n])
        print("*****\n")

print(">> number of matched lines: {ml}/{all}".format(ml=ccnt,all=numl))


