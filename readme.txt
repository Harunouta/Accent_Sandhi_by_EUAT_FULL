===============
必要なライブラリ
Mecab(-Overboseできるもの)(https://taku910.github.io/mecab/)
CRF++(https://taku910.github.io/crfpp/)
HTS_engine(http://hts-engine.sourceforge.net)
===============
必要なライブラリ(pip経由)
sinpleaudio
===============
必要なファイル等
unidic(ver2.3.0以降)
hts_voice用モデルファイル(日本語話者学習モデル)

Mecab辞書としてunidic-cwj-2.3-2.0(https://unidic.ninjal.ac.jp/download#unidic_bccwj)を
使用します。AddFileというディレクトリにダウンロードして解凍したファイル(unidic-cwj-2.3-2.0)を置いて下さい。
(システム辞書のデフォルトに設定する必要はありません。)
(別のversionのunidicを利用したい場合、Mecabespresso.pyの-dの参照するPATHを適宜置き換えてください。
なお作者の環境でunidic-cwj-3.1.0での動作も確認しています。FUll版じゃなくても動作します。)

音声を再生させたい場合、日本語話者の学習させたHTS_voiceモデル(meiとかm001-ATR503とか)が必要です。
AddFileというディレクトリに〇〇.htsvoiceというファイルを追加し、
EUAT2HTS.pyの該当項目を適宜書き換えて動かしてください。
==============
その他注意事項
Mecabespresso/Mecabespresso.py でMecabのコマンドを、
CRFsyori/CRFsyori.py および CRFsyori2/CRFsyori2.py CRFsyori3/CRFsyori3.py でCRF++のコマンドをEUAT2HTS.py でHTS_engineのコマンド
を呼び出しています。
コマンドラインの返却値を利用するので、pythonでのコマンドライン結果を取得できるpython環境でご利用ください。
(pyenvで指定されている場合は該当ディレクトリで設定されているpythonのパスと同じものを使用してください。)


ターミナルで
do.pyでCUI版を
GUI.pyでGUI版を実行できます。

本研究は名詞に限定した範囲で、
第83回情報処理学会全国大会(https://www.gakkai-web.net/gakkai/ipsj/83/program83.html#t4)
学生セッション［7N会場］（3月20日（土）　13:10〜15:10）
音声言語情報処理（2）
7N-02
アクセント単位形の推測を用いた日本語複合名詞のアクセント句の合成
○青柳詠美，小島正樹（東京薬科大）
で発表いたしました。

また全ての自立語を対象に
言語処理学会第28回年次大会(NLP2022)(https://www.anlp.jp/nlp2022/program.html#PT2-11)
ポスター番号　PT2-11（3月16日（水）　10:40〜12:00）
PT2-11	アクセント単位形の推測を用いた日本語複合語のアクセント句の合成
○青柳詠美, 小島正樹 (東薬大)
で発表いたします。

===========================
青柳　詠美
utaharunomar17@gmail.com
==========================