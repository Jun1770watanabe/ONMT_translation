import argparse
import os

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument("-i", '--input_path', type=str, help='Reference File')

    args = Argparser.parse_args()
    return args

args = argparser()

with open(args.input_path, encoding="utf-8") as f:
    sentences = f.readlines()

sentences = [" ".join(list(s)) for s in sentences]  
# output = os.path.splitext(os.path.basename(args.input_path))[0]
# output = "result/" + output + "_char.jp"
# output = "result/for_bleu/" + output + ".jp"
output = args.input_path

with open(output, 'w', encoding="utf-8") as f:
    f.write("".join(sentences))

