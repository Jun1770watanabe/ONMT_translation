python translate.py -model ./model/200326_wmt17_2000_step_500000.pt -src ./txt/wmt17/test.nm -tgt ./txt/wmt17/test.en > log/log_wmt17_2000.txt \
python translate.py -model ./model/200326_wmt17_280_step_100000.pt -src ./txt/wmt17/test.nm -tgt ./txt/wmt17/test.en > log/log_wmt17_280.txt \
python translate.py -model ./model/JESC_en_blstm_step_200000.pt -src ./txt/JESC/en_test.nm -tgt ./txt/JESC/test.en > log/log_JESC_en.txt /

