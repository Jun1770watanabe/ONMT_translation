#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from onmt.utils.logging import init_logger
from onmt.utils.misc import split_corpus
from onmt.translate.translator import build_translator

import onmt.opts as opts
from onmt.utils.parse import ArgumentParser

from tenkey_filter_V2 import KeyinputFilter
import socket


def Itranslate(opt):
    """ translate for interpreter Dialog version """
    ArgumentParser.validate_translate_opts(opt)
    logger = init_logger(opt.log_file)

    message = " $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n" + \
        " $$$  input ... alphabets or      $$$\n" + \
        " $$$           number sequence    $$$\n" + \
        " $$$  '5'...space   '6'...period  $$$\n" + \
        " $$$                              $$$\n" + \
        " $$$  if you want to exit,        $$$\n" + \
        " $$$      please input \"quit\"     $$$\n" + \
        " $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"

    temp = "txt/I_input.al"
    translator = build_translator(opt, report_score=False)

    addr = '192.168.12.218'
    port = 50000
    size = 1024

    while True:
        _addr = addr
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((_addr, port))
                s.listen(1)
                print(">> waiting for conection ...")
                conn, _addr = s.accept()
                print(">> conection successful.")
                conn.send(message.encode())

                while True:
                    conn.send("\n>> please input test sentence.".encode())
                    data = conn.recv(size)
                    test_sentence = data.decode()
                    print(test_sentence)

                    # alphabet to num
                    test_sentence = KeyinputFilter.alphab2num(test_sentence)

                    # process for error
                    test_sentence = test_sentence.replace('5', ' ')
                    if test_sentence == "":
                        continue

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

                    result = "\n--------------------------------------\n" + \
                        '# source : ' + test_sentence + '\n' + \
                        '# result : ' + result_sentence + '\n' + \
                        "--------------------------------------\n"

                    # conn.send(result.encode())
                    conn.send(result_sentence.encode())

        except Exception:
            print(">> disconnected.")



def _get_parser():
    parser = ArgumentParser(description='translate_v2.py')

    opts.config_opts(parser)
    opts.translate_opts(parser)
    return parser


def main():
    parser = _get_parser()

    opt = parser.parse_args()

    Itranslate(opt)


if __name__ == "__main__":
    main()
