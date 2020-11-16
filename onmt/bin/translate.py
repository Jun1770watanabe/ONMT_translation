#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from onmt.utils.logging import init_logger
from onmt.utils.misc import split_corpus
from onmt.translate.translator import build_translator

import onmt.opts as opts
from onmt.utils.parse import ArgumentParser

from tenkey_filter_V2 import KeyinputFilter
# from MCS import Comp_words
import numpy as np


def translate(opt):
    ArgumentParser.validate_translate_opts(opt)
    logger = init_logger(opt.log_file)

    translator = build_translator(opt, report_score=True)


    # # Misspelling Correction System
    # print(">> proccessing MCS ...")
    # with open(opt.src, encoding="utf-8") as f:
    #     text = f.readlines()
    # nw_list = []
    # for line in text:
    #     sentence = []
    #     for w in line.split(" "):
    #         sentence.append(Comp_words(w))
    #     nw_list.append(" ".join(sentence))
    # test_sentence = "\n".join(nw_list)

    # temp = "txt/test_temp.nm"
    # with open(temp, 'w', encoding="utf-8") as f:
    #     f.write(test_sentence) 

    print(">> translating ...")
    # src_shards = split_corpus(temp, opt.shard_size) # using MCS
    src_shards = split_corpus(opt.src, opt.shard_size) # without MCS

    tgt_shards = split_corpus(opt.tgt, opt.shard_size)
    shard_pairs = zip(src_shards, tgt_shards)

    for i, (src_shard, tgt_shard) in enumerate(shard_pairs):
        logger.info("Translating shard %d." % i)
        _, pred_sents = translator.translate(
            src=src_shard,
            tgt=tgt_shard,
            src_dir=opt.src_dir,
            batch_size=opt.batch_size,
            batch_type=opt.batch_type,
            attn_debug=opt.attn_debug,
            align_debug=opt.align_debug,
            )
    
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


def check_quit(text):
    text = text.lower()
    if text == "quit":
        print(">> Exit this program.")
        print(">> bye.")
        exit()

def Itranslate(opt):
    """ translate for interpreter Dialog version """
    ArgumentParser.validate_translate_opts(opt)
    logger = init_logger(opt.log_file)

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$  input ... alphabets or      $$$")
    print("$$$           number sequence    $$$")
    print("$$$  '5'...space   '6'...period  $$$")
    print("$$$                              $$$")
    print("$$$  if you want to exit,        $$$")
    print("$$$      please input \"quit\"     $$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    temp = "txt/I_input.al"
    translator = build_translator(opt, report_score=False)

    while True:
        print(">> please input test sentence.")
        test_sentence = input()
        check_quit(test_sentence)

        # alphabet to num
        test_sentence = KeyinputFilter.alphab2num(test_sentence)

        # process for error
        test_sentence = test_sentence.replace('5', ' ')
        if test_sentence == "":
            continue

        # # Misspelling Correction System
        # nw_list = []
        # print(test_sentence)
        # for w in test_sentence.split(" "):
        #     nw_list.append(Comp_words(w))
        # test_sentence = " ".join(nw_list)
        # print(test_sentence)

        with open(temp, 'w', encoding="utf-8") as f:
            f.write(test_sentence)

        src_shards = split_corpus(temp, opt.shard_size)
        tgt_shards = split_corpus(opt.tgt, opt.shard_size)
        shard_pairs = zip(src_shards, tgt_shards)

        for i, (src_shard, tgt_shard) in enumerate(shard_pairs):
            _, pred_sents = translator.translate(
                src=src_shard,
                tgt=tgt_shard,
                src_dir=opt.src_dir,
                batch_size=opt.batch_size,
                batch_type=opt.batch_type,
                attn_debug=opt.attn_debug,
                align_debug=opt.align_debug
                )
            
        result_sentence = pred_sents[0][0]

        print("--------------------------------------")
        print('# source : ' + test_sentence)
        print('# result : ' + result_sentence)
        print("--------------------------------------")


def _get_parser():
    parser = ArgumentParser(description='translate.py')

    opts.config_opts(parser)
    opts.translate_opts(parser)
    return parser


def main():
    parser = _get_parser()

    opt = parser.parse_args()

    if opt.src is not None:
        translate(opt)
    else:
        Itranslate(opt)


if __name__ == "__main__":
    main()
