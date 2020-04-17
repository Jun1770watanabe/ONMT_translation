OpenNMTを用いた翻訳プログラム
（学習のみに関わるファイルは省いている）

〇translate.pyについて
-src，-tgt オプションでテキストファイル（./txt以下のテストデータ）を指定することによってファイルからの翻訳が可能．
（-srcと-tgtの両方を指定する必要有）
この時，data_.txtというファイルが自動生成される．
これは，プロット用のデータをリストで保存しているファイルであり，単語正解精度，語数の分布などが含まれる．
テキストファイルを指定しない場合，自動的に対話形式でプログラムが動作する．
対話形式の場合，便宜的にアルファベット入力が可能．
（入力されたアルファベットを数値列に変換してから翻訳している．）
"quit" と入力するとプログラムを終了する．
どちらにしても，-model引数でモデルを指定しなければエラー．



〇translate_v2.pyについて
translate_v2.py はソケット通信に対応した翻訳プログラム．
対話形式でのみ実行可能，ファイル入出力非対応．
（この場合，translate_v2がサーバプログラムとなる．client.pyでテスト可能．）
実行時，必ず-model引数でモデルを指定．



〇モデルについて
./model/以下

model/200326_wmt17_280　　wmt17データセットから280万文学習
model/200326_wmt17_2000　wmt17データセットから2000万文学習
model/JESC_en_blstm　　　JESCの英語（280万文）
model/kanji_blstm　　　　JESCの日本語（280万文）



〇テストデータについて
./txt/以下
拡張子に注意すること．

en  英語テキストファイル
jp　日本語テキストファイル
nm　数値列テキストファイル

・対訳データ（JESC日本語）
txt/JESC/test.jp
txt/JESC/jp_test.nm

・対訳データ（JESC英語）
txt/JESC/test.en
txt/JESC/en_test.nm

・対訳データ（wmt17）
txt/wmt17/test.en
txt/wmt17/test.nm



〇その他プログラムについて
ほぼ全てonmt以下にある
デバッグには ./onmt/bin/translate* を見る必要がある場合がある．


＝＝＝＝＝以下，実行例＝＝＝＝＝＝＝＝＝＝＝

【ソケット通信版】
python .\translate_v2.py -model .\model\200326_wmt17_2000_step_500000.pt


【テストデータ：JESC】
python .\translate.py -model .\model\200326_wmt17_2000_step_500000.pt -src .\txt\JESC\en_test.nm -tgt .\txt\JESC\test.en
python .\translate.py -model .\model\200326_wmt17_280_step_70000.pt -src .\txt\JESC\en_test.nm -tgt .\txt\JESC\test.en


【テストデータ：wmt17】
python .\translate.py -model .\model\200326_wmt17_2000_step_500000.pt -src .\txt\wmt17\test.nm -tgt .\txt\wmt17\test.en
python .\translate.py -model .\model\200326_wmt17_280_step_70000.pt -src .\txt\wmt17\test.nm -tgt .\txt\wmt17\test.en