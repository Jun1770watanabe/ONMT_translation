import argparse

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument("-i", '--input', type=str, help='Reference File')

    args = Argparser.parse_args()
    return args

args = argparser()

with open(args.input, encoding="utf-8") as f:
    sentences = f.readlines()

sentences = [list(s.replace(" ", "")) for s in sentences]  
sentences = [" ".join(s) for s in sentences]

output = os.path.splitext(os.path.basename(opt.models[0]))[0]
output = "result/" + output + ".jp"
with open(output, 'w', encoding="utf-8") as f:
    f.write("".join(sentences))

