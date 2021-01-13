import sys, io
import argparse
import pprint as pp

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
        # pp.pprint(cost)
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

def calc_all(hyp_filename, ref_filename):
    with open(ref_filename, encoding="utf-8", errors='backslashreplace') as f:
        ref_data = f.readlines()
    with open(hyp_filename, encoding="utf-8", errors='backslashreplace') as f:
        hyp_data = f.readlines()

    acc_list = []
    for k in range(len(ref_data)):
        ali = dp(ref_list=ref_data[k].split(), hyp_list=hyp_data[k].split())
        acc = 100.0 * ali["ALI"].count("C") / len(ali["ALI"])
        # if acc == 0:
        #     pp.pprint(ali)
        acc_list.append(acc)
    print(">> Average : {:.2f}%".format(sum(acc_list)/len(acc_list)))
    return

def test_dp():
    ali = dp(ref_list=['a', 'b', 'c', 'c', 'd', 'f', 'g'],
             hyp_list=['a', 'c', 'd', 'e', 'g', 'k'])
    print("REF: " + " | ".join(ali["REF"]))
    print("HYP: " + " | ".join(ali["HYP"]))
    print("ALI: " + " | ".join(map(lambda x: "{:3s}".format(x), ali["ALI"])))

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    parser = argparse.ArgumentParser(description='Julius Scoring Tool')
    parser.add_argument('mode', help='Mode', choices=['_test', 'from_file'])
    parser.add_argument('--ref', help='Input Reference file', default="ref.txt")
    parser.add_argument('--hyp', help='Input Hypothesis file', default="hyp.txt")
    args = parser.parse_args()
    if args.mode == "_test":
        test_dp()
    elif args.mode == "from_file":
        calc_all(args.hyp, args.ref)