# -*- coding: utf-8 -*-
#元ソース:jpcommon_rule_shift_jis.h
#moradic


def moraDic(mora):
    prondic=["*","pau","ヴョ","ヴュ","ヴャ","ヴォ","ヴェ","ヴィ","ヴァ","ヴ",\
             "ン","ヲ","ヱ","ヰ","ワ","ヮ",\
             "ロ","レ","ル","リョ","リュ","リャ","リェ","リ","ラ",\
             "ヨ","ョ","ユ","ュ","ヤ","ャ",\
             "モ","メ","ム","ミョ","ミュ","ミャ","ミェ","ミ","マ",\
             "ポ","ボ","ホ","ペ","ベ","ヘ",\
             "プ","ブ","フォ","フェ","フィ","ファ","フ",\
             "ピョ","ピュ","ピャ","ピェ","ピ","ビョ","ビュ","ビャ","ビェ","ビ","ヒョ","ヒュ","ヒャ","ヒェ","ヒ","パ","バ","ハ",\
             "ノ","ネ","ヌ","ニョ","ニュ","ニャ","ニェ","ニ","ナ",\
             "ドゥ","ド","トゥ","ト","デョ","デュ","デャ","ディ","デ","テョ","テュ","テャ","ティ","テ",\
             "ヅ","ツォ","ツェ","ツィ","ツァ","ツ","ッ",\
             "ヂ","チョ","チュ","チャ","チェ","チ","ダ","タ",\
             "ゾ","ソ","ゼ","セ","ズィ","ズ","スィ","ス",\
             "ジョ","ジュ","ジャ","ジェ","ジ","ショ","シュ","シャ","シェ","シ","ザ","サ",\
             "ゴ","コ","ゲ","ケ","ヶ","グヮ","グ","クヮ","ク",\
             "ギョ","ギュ","ギャ","ギェ","ギ",\
             "キョ","キュ","キャ","キェ","キ","ガ","カ",\
             "オ","ォ","エ","ェ","ウォ","ウェ","ウィ","ウ","ゥ",\
             "イェ","イ","ィ","ア","ァ",\
             "a","i","u","e","o"]
    romandic=[["*"],["pau"],["by","o"],["by","u"],["by","a"],["v","o"],["v","e"],["v","i"],["v","a"],["v","u"],\
              ["N"],["o"],["e"],["i"],["w","a"],["w","a"],\
              ["r","o"],["r","e"],["r","u"],["ry", "o"],["ry", "u"],["ry","a"],["ry","e"],["r","i"],["r","a"],\
              ["y","o"],["y","o"],["y","u"],["y","u"],["y","a"],["y","a"],\
              ["m", "o"],["m","e"],["m","u"],["my","o"],["my","u"],["my","a"],["my","e"],["m","i"],["m","a"],\
              ["p","o"],["b","o"],["h","o"],["p","e"],["b","e"],["h","e"],\
              ["p","u"],["b","u"],["f","o"],["f","e"],["f","i"],["f","a"],["f", "u"],\
              ["py","o"],["py","u"],["py","a"],["py","e"],["p","i"],["by","o"],["by","u"],["by","a"],["by","e"],["b","i"],["hy","o"],["hy","u"],["hy","a"],["hy","e"],["h","i"],["p","a"],["b","a"],["h","a"],\
              ["n","o"],["n","e"],["n","u"],["ny","o"],["ny","u"],["ny","a"],["ny","e"],["n","i"],["n","a"],\
              ["d","u"],["d","o"],["t","u"],["t","o"],["dy","o"],["dy","u"],["dy","a"],["d","i"],["d","e"],["ty","o"],["ty","u"],["ty","a"],["t","i"],["t","e"],\
              ["z","u"],["ts", "o"],["ts","e"],["ts","i"],["ts","a"],["ts","u"],["cl"],\
              ["j","i"],["ch","o"],["ch","u"],["ch","a"],["ch","e"],["ch","i"],["d","a"],["t","a"],\
              ["z","o"],["s","o"],["z","e"],["s","e"],["z","i"],["z","u"],["s","i"],["s","u"],\
              ["j","o"],["j","u"],["j","a"],["j","e"],["j","i"],["sh","o"],["sh","u"],["sh","a"],["sh","e"],["sh","i"],["z","a"],["s","a"],\
              ["g","o"],["k","o"],["g","e"],["k","e"],["k","e"],["gw","a"],["g","u"],["kw","a"],["k","u"],\
              ["gy","o"],["gy","u"],["gy","a"],["gy","e"],["g","i"],\
              ["ky","o"],["ky","u"],["ky","a"],["ky","e"],["k","i"],["g","a"],["k","a"],\
              ["o"],["o"],["e"],["e"],["w","o"],["w","e"],["w","i"],["u"],["u"],\
              ["y","e"],["i"],["i"],["a"],["a"],\
              ["a"],["i"],["u"],["e"],["o"]]
    roma=romandic[prondic.index(mora)]
    return roma
"""
txt=["チャ","ン","ネ","ル"]

for n in range(len(txt)):
    print(moraDic(txt[n]))


['ch', 'a']
['N']
['n', 'e']
['r', 'u']
"""
#posTypeDic
#pos1	品詞大分類
#pos2	品詞中分類
#pos3	品詞小分類
#pos4	品詞細分類
#cType	活用型
#cForm	活用形

def posDic(pos1,pos2,pos3):
    if pos1=="名詞":
        if pos2=="普通名詞":
            if pos3=="一般":
                PosToDic="02"
            else:
                PosToDic="03"
        elif pos2=="固有名詞":
            PosToDic="18"
        elif pos2=="数詞":
            PosToDic="05"
        else:
            PosToDic="02"
    elif pos1=="代名詞":
        PosToDic="04"
    elif pos1=="形状詞":
        PosToDic="19"
    elif pos1=="連体詞":
        PosToDic="07"
    elif pos1=="副詞":
        PosToDic="06"
    elif pos1=="接続詞":
        PosToDic="08"
    elif pos1=="感動詞":
        if pos2=="一般":
            PosToDic="09"
        else:
            PosToDic="25"
    elif pos1=="動詞":
        if pos2=="一般":
            PosToDic="20"
        else:
            PosToDic="17"
    elif pos1=="形容詞":
        PosToDic="01"
    elif pos1=="助動詞":
        PosToDic="10"
    elif pos1=="助詞":
        if pos2=="格助詞":
            PosToDic="23"
        elif pos2=="副助詞":
            PosToDic="11"
        elif pos2=="係助詞":
            PosToDic="24"
        elif pos2=="接続助詞":
            PosToDic="12"
        elif pos2=="終助詞":
            PosToDIc="14"
        else:
            PosToDic="23"
    elif pos1=="接頭辞":
        PosToDic="16"
    elif pos1=="接尾辞":
        PosToDic="15"
    else:
        PosToDIc=="xx"
            
    return PosToDic

def cTypeDic(cType):
    if "*" in cType:
        cTypeToDic="xx"
    elif "カ行変格" in cType:
        cTypeToDic="5"
    elif "サ行変格" in cType:
        cTypeToDic="4"
    elif "ラ行変格" in cType:
        cTypeToDic="6"
    elif "一段" in cType:
        cTypeToDic="3"
    elif "形容詞" in cType:
        cTypeToDic="7"
    elif "五段" in cType:
        cTypeToDic="1"
    elif "四段" in cType:
        cTypeToDic="6"
    elif "助動詞" in cType:
        cTypeToDic="7"
    elif "二段" in cType:
        cTypeToDic="6"
    elif "不変化" in cType:
        cTypeToDic="6"
    elif "文語助動詞" in cType:
        cTypeToDic="6"
    else:
        cTypeToDic="xx"
    return cTypeToDic

def cFormDic(cForm):
    if "*" in cForm:
        cFormToDic="xx"
    if "その他" in cForm:
        cFormToDic="6"
    if "仮定形" in cForm:
        cFormToDic="4"
    if "基本形" in cForm:
        cFormToDic="2"
    if "未然形" in cForm:
        cFormToDic="0"
    if "命令形" in cForm:
        cFormToDic="5"
    if "連体形" in cForm:
        cFormToDic="3"
    if "連用形" in cForm:
        cFormToDic="1"
    else:
        cFormToDic="xx"
    return cFormToDic

#if __name__ == "__main__":
#    main()
