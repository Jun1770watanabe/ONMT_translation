import sys, io
import argparse
import re
import pprint as pp
import json

# DP matching for word alignment
def dp(*, ref_list, hyp_list):
    ref_list = ['sil'] + ref_list
    hyp_list = ['sil'] + hyp_list
    ref_len = len(ref_list)
    hyp_len = len(hyp_list)
    # Initailize cost matrix
    #   The 1st-row and -column is always substituted because of "sil"
    cost = [[0 for i in range(ref_len)] for j in range(hyp_len)]
    cost[0][0] = 0
    for i in range(1, ref_len):
        cost[0][i] = 1 + cost[0][i-1]
    for j in range(1, hyp_len):
        cost[j][0] = 1 + cost[j-1][0]
    # Calculate cost with Dynamic Programming
    for i in range(1, ref_len):
        for j in range(1, hyp_len):
            # Correct, or Substituion error
            cur_cost  = cost[j-1][i-1] + (ref_list[i] != hyp_list[j])
            # Or, Insertion error?
            cur_cost = min([cost[j-1][i] + 1, cur_cost])
            # Or, Deletion error?
            cur_cost = min([cost[j][i-1] + 1, cur_cost])
            # Update to the minimal cost
            cost[j][i] = cur_cost
        #pp.pprint(cost)
    # Backtrace
    aligned_hyp_list = []
    aligned_ref_list = []
    aligned_eval_list = []
    i, j = [ref_len-1, hyp_len-1]
    while (i > 0) or (j > 0):
        if cost[j][i] == cost[j-1][i]+1:
            aligned_eval_list.append('I')
            aligned_ref_list.append('<eps>')
            aligned_hyp_list.append(hyp_list[j])
            j-=1
        elif cost[j][i] == cost[j][i-1]+1:
            aligned_eval_list.append('D')
            aligned_ref_list.append(ref_list[i])
            aligned_hyp_list.append('<eps>')
            i-=1
        elif cost[j][i] == cost[j-1][i-1]+1:
            aligned_eval_list.append('S')
            aligned_ref_list.append(ref_list[i])
            aligned_hyp_list.append(hyp_list[j])
            i-=1
            j-=1
        elif cost[j][i] == cost[j-1][i-1]:
            aligned_eval_list.append('C')
            aligned_ref_list.append(ref_list[i])
            aligned_hyp_list.append(hyp_list[j])
            i-=1
            j-=1
        else:
            print("U {:d}, {:d}".format(j, i))
    aligned_ref_list.reverse()
    aligned_hyp_list.reverse()
    aligned_eval_list.reverse()
    return {
        "REF": aligned_ref_list,
        "HYP": aligned_hyp_list,
        "ALI": aligned_eval_list
    }
# Guess encoding
def guess_charset(filename):
    _max_item = lambda d: max(d.items(), key=lambda x: x[1])[0]
    th = 0.99
    charsets = ['utf8', 'cp932', 'ujis', 'iso2022jp']
    counts = {key: 1 for key in charsets}
    with open(filename, 'rb') as f:
        for line in f:
            # skip ascii-only strings
            try:
                line.decode('ascii', errors="strict")
                continue
            except UnicodeDecodeError: pass
            # check encoding
            for c in charsets:
                try:
                    line.decode(c)
                    counts[c] += len(line)
                    break
                except UnicodeDecodeError: pass
            # finish?
            if th < max(counts.values()) / sum(counts.values()):
                break
    return _max_item(counts)
def cmd_res2hyp(res_filename, target=r'sentence'):
    with open(res_filename, 'r', encoding=guess_charset(res_filename), errors='backslashreplace') as f:
        for line in f:
            # extract file id
            m1 = re.search(r'speechfile: (.*)\..*$', line)
            if m1:
                print(m1.group(1) + '\t', end='')
            m2 = re.search(r'{0}\d+:\s*(.*)$'.format(target), line)
            if m2:
                if target == 'phseq':
                    str = m2.group(1).replace('| ', '')  # Juliusの音素表記の縦棒は不要
                    str = re.sub(r'_.', '', str)   # Julius DNNの音素表記sufiix(*_I, *_B)を除く
                    print(str, end='\n')
                else:
                    print(m2.group(1), end='\n')
    return
def cmd_align(hyp_filename, ref_filename, eval_target):
    # Load reference file
    ref_data = {}
    with open(ref_filename, 'r', encoding=guess_charset(ref_filename), errors='backslashreplace') as f:
        for line in f:
# by me 0_0
# accept blank txt
            if re.match(r'^ \d+\t.+$',line) is None:
              id = line.strip()
              txt = ""
            else:
              id, txt = line.split(None, 1)
            words = txt.rstrip().split(' ')
            ref_data[id] = words
    # Load hypothesis file: converted from julius's raw result file by res2hyp
    hyp_data = {}
    with open(hyp_filename, 'r', encoding=guess_charset(hyp_filename), errors='backslashreplace') as f:
        for line in f:
# by me 0_0
# accept blank txt
            if re.match(r'^ \d+\t.+$',line) is None:
              id = line.strip()
              txt = ""
            else:
              id, txt = line.split(None, 1)
            words = txt.rstrip().split(' ')
            hyp_data[id] = words
    # Print the aligned word sequence by DP matching (DTW)
    for k in hyp_data.keys():
        ali = dp(ref_list=ref_data[k], hyp_list=hyp_data[k])
        print(k)
# by me 0_0
# Delete element that do not relate to eval
        if eval_target == "border":
          for idx in reversed(range(len(ali["REF"]))):
            if ali["REF"][idx] != "/" and ali["HYP"][idx] != "/" and ali["REF"][idx] != "@" and ali["HYP"][idx] != "@" and ali["REF"][idx] != "." and ali["HYP"][idx] != ".":
              del ali["REF"][idx]
              del ali["HYP"][idx]
              del ali["ALI"][idx]
        elif eval_target == "core":
          for idx in reversed(range(len(ali["REF"]))):
            if "'" not in ali["REF"][idx] and "'" not in ali["HYP"][idx]:
              del ali["REF"][idx]
              del ali["HYP"][idx]
              del ali["ALI"][idx]
        print("REF: " + "\t| ".join(ali["REF"]))
        print("HYP: " + "\t| ".join(ali["HYP"]))
        print("ALI: " + "\t| ".join(map(lambda x: "{:3s}".format(x), ali["ALI"])))
        print('JSON: {"id": "' + k + '", "alignment": ' + json.dumps(ali, ensure_ascii=False) + "}")
def cmd_score(ali_filename):
    # Load alignment file
    ali_data = []
    with open(ali_filename, 'r', encoding=guess_charset(ali_filename), errors='backslashreplace') as f:
        for line in f:
            m1 = re.match(r'JSON: (.*)$', line)
            if not m1:
                continue
            data = json.loads(m1.group(1))
            ali_data.append(data)
#    print(ali_data)
    # Count results
    num = {
        "Words": 0, "Sentences": 0,
        "C": 0, "S": 0, "D": 0, "I": 0
        }
    for datum in ali_data:
        num["Sentences"] += 1
        for alires in datum["alignment"]["ALI"]:
            num[alires] += 1
            num["Words"] += 1 if alires != "I" else 0
    # Output summary of scores
    print("Num of sentences and words: {Sentences:d}, {Words:d}".format(**num))
    print("Num of C, S, D and I      : {C:d}, {S:d}, {D:d}, {I:d}".format(**num))
    print("Word correct rate         : {:.1f}%".format(100.0*num["C"]/num["Words"]))
    print("Word accuray              : {:.1f}%".format(100.0*(num["C"]-num["I"])/num["Words"]))
    print("Word Error rate           : {:.1f}%".format(100.0*(num["S"]+num["D"]+num["I"])/num["Words"]))
def _test_dp():
    ali = dp(ref_list=['a', 'b', 'c', 'c', 'd', 'f', 'g'],
                hyp_list=['a', 'c', 'd', 'e', 'g', 'k'])
    print("REF: " + " | ".join(ali["REF"]))
    print("HYP: " + " | ".join(ali["HYP"]))
    print("ALI: " + " | ".join(map(lambda x: "{:3s}".format(x), ali["ALI"])))
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    parser = argparse.ArgumentParser(description='Julius Scoring Tool')
    parser.add_argument('mode', help='Mode', choices=['res2hyp', 'align', 'score', '_test'])
    parser.add_argument('--res', help='Input Julius\'s result file', default="result.txt")
    parser.add_argument('--ref', help='Input Reference file', default="ref.txt")
    parser.add_argument('--hyp', help='Input Hypothesis file', default="hyp.txt")
    parser.add_argument('--ali', help='Input Alignment file', default="ali.txt")
    parser.add_argument('--target', help='Target of results', default="sentence", choices=["sentence", "phseq", "wseq"])
    parser.add_argument('--eval', help='Target of evaluation', default="all", choices=["all", "border", "core"])
    args = parser.parse_args()
    if args.mode == "res2hyp":
        cmd_res2hyp(args.res, args.target)
    elif args.mode == "align":
        cmd_align(args.hyp, args.ref, args.eval)
    elif args.mode == "score":
        cmd_score(args.ali)
    elif args.mode == "test":
        _test_dp()