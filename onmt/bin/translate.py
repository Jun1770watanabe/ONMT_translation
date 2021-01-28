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
import os

def translate(opt):
    ArgumentParser.validate_translate_opts(opt)
    logger = init_logger(opt.log_file)

    translator = build_translator(opt, report_score=False)

    print(">> translating ...")
    src_shards = split_corpus(opt.src, opt.shard_size)
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

    output_result = os.path.splitext(os.path.basename(opt.models[0]))[0]
    output_result = "result/" + output_result + ".jp"
    pred_sents = [s[0] for s in pred_sents]
    with open(output_result, 'w', encoding="utf-8") as f:
        f.write("\n".join(pred_sents))
    exit()


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
