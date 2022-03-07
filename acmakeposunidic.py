# -*- coding: utf-8 -*-
#unidicやOPEN J TALKで言われているアクセントの結合法則を元論文から再現
#元論文[日本語単語連鎖のアクセント規則]
from Mecabespresso import Mecabespresso
from SAGISAKA import SAGISAKA
from MIYAZAKI import MIYAZAKI
from YURAGI import YURAGI
from CRFsyori3 import CRFsyori3

#アクセント結合方法
"""
自分の考えているアクセント仕様
1.基本的には全て繋げる(unidicの仕様通り)(?どこまで先にルールとして行う？)
2.CRFで乖離が予測され、強調条件の場合、単独アクセント句(?)に

"""

def acmake(word,strong):
    #mecabの結果から実際に抽出する
    #word="第一回目"
    Mecabespresso.sentence(word)
    with open ("Mecabespresso/split.txt","r",encoding="UTF-8") as f:
        line=f.readlines()

    #CRFの結果を取ってくる
    SUW=[]
    pos=[]
    Type=[]
    Form=[]
    poss=[]
    kana=[]
    #Pho=[]
    for n in range(len(line)):
        if line[n]!="EOS\n":
            SUW.append(Mecabespresso.surface(line[n]))
            pos.append(Mecabespresso.pos1(line[n]))
            #Pho.append(Mecabespresso.pron(line[n]))
            if "-" in Mecabespresso.cType(line[n]):
                Type.append(Mecabespresso.cType(line[n]).split("-")[1]+Mecabesplesso.cType(line[n]).split("-")[0])
                Form.append(Mecabespresso.cForm(line[n]).split("-")[0])
            else:
                Type.append(Mecabespresso.cType(line[n]))
                Form.append(Mecabespresso.cForm(line[n]))
            poss.append(Mecabespresso.pos2(line[n]))
            if "・" in Mecabespresso.kana(line[n]):
                kana.append(Mecabespresso.pron(line[n]))
            else:
                kana.append(Mecabespresso.kana(line[n]))
    
    CRFS=CRFsyori3.CRFbox(SUW,pos,Type,Form,poss,kana)
        #print(SUW)


    #アクセント句の推定
    ku=[]
    for n in range(len(CRFS)):
        if CRFS[n]=="1" and strong[n]=="1":
            ku.append(1)
        else:
            ku.append(0)
    #print("accent:"+str(ku))


    #アクセント合成==================================
    zenbu=int(Mecabespresso.acseiri(Mecabespresso.aType(line[0])))
    propho=Mecabespresso.pron(line[0])
    suw=Mecabespresso.surface(line[0])

    #M優先
    acbox=[]
    readbox=[]
    suwbox=[]
    if Mecabespresso.aModType(line[0])!="":
        zenbu=SAGISAKA.M(Mecabespresso.mora(propho),zenbu,Mecabespresso.aModType(line[0]))
    for n in range(len(line)-1):#bi-gram
        if "EOS" in line[n+1]:#終了
            #print(Mecabespresso.surface(line[n]))
            #print(Mecabespresso.surface(line[n+1]))
            #print(zenbu)
            #print("===================================")
            #print(SUW)
            #print(kana)
            acbox.append(zenbu)
            #print(acbox)
            readbox.append(propho)
            #print(readbox)
            suwbox.append(suw)
            #print(suwbox)

            return [acbox,readbox,suwbox]
            
        elif n==0 and ku[n]==1:#先頭アクセントが独立のとき
            zenbu=int(Mecabespresso.acseiri(Mecabespresso.aType(line[n])))
            if len(YURAGI.morabox(propho))>1 and zenbu==0:
                zenbu=len(YURAGI.morabox(propho))
            if len(YURAGI.morabox(propho))>1:#独立句のアクセント核が0のとき
                zenbu=YURAGI.wave(YURAGI.morabox(propho),zenbu)
            acbox.append(zenbu)#独立アクセント句を書き出す
            zenbu=int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1])))
            propho=Mecabespresso.pron(line[n+1])
            suw=Mecabespresso.surface(line[n+1])
            readbox.append(Mecabespresso.pron(line[n]))
            suwbox.append(Mecabespresso.surface(line[n]))
            
            
        elif ku[n]==1:#独立後のアクセント
            acbox.append(zenbu)
            readbox.append(propho)
            suwbox.append(suw)
            zenbu=int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1])))
            propho=Mecabespresso.pron(line[n+1])
            suw=Mecabespresso.surface(line[n+1])

        else:
            #アクセント句の抽出
            m1=zenbu
            m2=Mecabespresso.acseiri(Mecabespresso.aType(line[n+1]))
            #M優先
            if Mecabespresso.aModType(line[n+1])!="":
                m2=SAGISAKA.M(Mecabespresso.mora(Mecabespresso.pron(line[n+1])),int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1]))),Mecabespresso.aModType(line[n+1]))
            #数詞結合法則
            suu=""
            #数詞+助数詞
            suu=MIYAZAKI.MIYAZAKI(Mecabespresso.mora(propho),Mecabespresso.mora(Mecabespresso.pron(line[n+1])),Mecabespresso.orth(line[n+1]),Mecabespresso.orth(line[n]),Mecabespresso.iConType(line[n]))
            #アクセント結合(数詞結合法則で載っていなかったら)
            if suu=="":#MIYAZAKI.pyに該当部分がなかったらSAGISAKA.py
                if "P" in Mecabespresso.aConType(line[n]):#接頭辞
                    zenbu=SAGISAKA.P(Mecabespresso.mora(propho),Mecabespresso.mora(Mecabespresso.pron(line[n+1])),zenbu,int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1]))),Mecabespresso.aConType(line[n]))
                elif "C" in Mecabespresso.aConType(line[n+1]):
                    zenbu=SAGISAKA.C(Mecabespresso.mora(propho),zenbu,int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1]))),Mecabespresso.aConType(line[n+1]))
                elif Mecabespresso.pos1(line[n+1]) in Mecabespresso.aConType(line[n+1]):#該当品詞が無かったらN
                    zenbu=SAGISAKA.F(Mecabespresso.mora(propho),zenbu,Mecabespresso.aConType(line[n+1]),Mecabespresso.pos1(line[n+1]))
                else:
                    zenbu=SAGISAKA.N(Mecabespresso.mora(propho),Mecabespresso.mora(Mecabespresso.pron(line[n+1])),zenbu,int(Mecabespresso.acseiri(Mecabespresso.aType(line[n+1]))))
            else:
                zenbu=suu
            #print(suu)
            #print(propho)    
            propho=propho+Mecabespresso.pron(line[n+1])
            suw=suw+Mecabespresso.surface(line[n+1])
            zenbu=YURAGI.wave(YURAGI.morabox(propho),zenbu)
            #print(Mecabespresso.surface(line[n+1]))
            #print(zenbu)
