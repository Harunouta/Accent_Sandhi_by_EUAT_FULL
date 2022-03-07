# -*- coding: utf-8 -*-
#推測アクセント句をHTS_engineで読ませる
#予めopenjtalk(HTS_engineが呼べればそれ以外でも可)とHTS用日本語発話モデルファイルが必要
#元論文　HTS-demo_NIT-ATR503-M001/data/lab_format.pdf "An example of context-dependent label format for HMM-based speech synthesis in Japanese"

#=You set model path!=
#=HTS_voiceモデルを指定してくりょ=
#voice="AddFile/mei_normal.htsvoice"
voice="/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_normal.htsvoice"
#===========


#$"hts_engine -m"+HTS_model+" -ow out.wav id2.txt"

import simpleaudio
import subprocess
from Mecabespresso import Mecabespresso
from HTSDictyonary import HTSDictionary 


#MoraAndSuw(pos)
#morasuw:各モーラを格納
#suwdic:各モーラがSUWの何番目かを格納
def MakeSuwDic():
    morasuw=[]
    suwdic=[]
    with open ("Mecabespresso/split.txt","r",encoding = "UTF-8") as f:
        line = f.readlines()
    prepron=""
    for n in range(len(line)-1):
        for m in range(len(Mecabespresso.pron(line[n]))):
            nowpron=Mecabespresso.pron(line[n])[m]
            if nowpron in ["ァ","ィ","ゥ","ェ","ォ","ャ","ュ","ョ"]:
                nowpron=prepron+nowpron
            if m!=len(Mecabespresso.pron(line[n]))-1:
                if Mecabespresso.pron(line[n])[m+1] not in ["ァ","ィ","ゥ","ェ","ォ","ャ","ュ","ョ"]:
                    morasuw.append(nowpron)
                    suwdic.append(n)
            else:
                morasuw.append(nowpron)
                suwdic.append(n)
            prepron=nowpron

            
    return morasuw,suwdic

#MoraAndAcc
#moraacc:各モーラごとのアクセント核の位置
#accdic:([モーラ],[(アクセント句番号)~(通しモーラ数)~(アクセント核番号)])
#accmora:[各アクセント句のモーラ数,各アクセント句のモーラ数]
def AccDic(readbox,acbox):
    moraacc=[]
    accdic=[]
    prepron=""
    for n in range(len(readbox)):
        for m in range(len(readbox[n])):
            nowpron=readbox[n][m]
            if nowpron in ["ァ","ィ","ゥ","ェ","ォ","ャ","ュ","ョ"]:
                nowpron=prepron+nowpron
            if m!=len(readbox[n])-1:
                if readbox[n][m+1] not in ["ァ","ィ","ゥ","ェ","ォ","ャ","ュ","ョ"]:
                    moraacc.append(nowpron)
                    accdic.append(str(n)+"~"+str(m+1)+"~"+str(acbox[n]))
            else:
                moraacc.append(nowpron)
                accdic.append(str(n)+"~"+str(m+1)+"~"+str(acbox[n]))
            prepron=nowpron
    accmora=[]
    accdic2=[]
    for m in range(len(accdic)):
        accdic2.append(accdic[m].split("~")[0])
    ackind=sorted(list(set(accdic2)),reverse=False)
    #print(ackind)
    for n in range(len(ackind)):
        accmora.append(accdic2.count(ackind[n]))
    return moraacc,accdic,accmora

#strong考慮(pauが入る)
#morasuw:pauを考慮したモーラを格納
#suwdic:pauを考慮したSUWで何晩目になるかを記載
#accdic:pauを考慮したacc関連を格納(詳細がは上記同項目を参照)
def reroadByStrong(strong,morasuw,suwdic,accdic):
    prenum=0
    for n in range(len(suwdic)):
        if n!=len(suwdic)-1:
            if prenum!=suwdic[n+1]:
                prenum=suwdic[n+1]
                if strong[int(suwdic[n+1])]=="1":
                    morasuw[n+1:n+1]=["pau"]
                    suwdic[n+1:n+1]=[suwdic[n]]
                    accdic[n+1:n+1]=[accdic[n]]
                if strong[int(suwdic[n])]=="1":
                    morasuw[n+1:n+1]=["pau"]
                    suwdic[n+1:n+1]=[suwdic[n]]
                    accdic[n+1:n+1]=[accdic[n]]
                
    return morasuw,suwdic,accdic

#pho変換
#pho:読み(最初の呼吸や捨て文字xx含む)
#newsuwdic:phoごとにSUWで何番目かを格納
#newaccdic:phoごとにアクセント句でも通し番号~アクセント句中のモーラ数~アクセント句中のモーラごとの通し番号
def reroadByPho(morasuw,suwdic,accdic):
    pho=["xx","xx","sil"]
    newsuwdic=["xx","xx","xx"]
    newaccdic=["xx","xx","xx"]
    for n in range(len(morasuw)):
        if morasuw[n]=="ー":
            morasuw[n]=pho[-1]
        expho=HTSDictionary.moraDic(morasuw[n])
        pho.extend(expho)
        for m in range(len(expho)):
            newsuwdic.append(suwdic[n])
            newaccdic.append(accdic[n])
    pho.extend(["sil","xx","xx"])
    newsuwdic.extend(["xx","xx","xx"])
    newaccdic.extend(["xx","xx","xx"])
    return pho,newsuwdic,newaccdic

#=Write_HTS-label=
def MakeHTSID(pretime,accmora,\
             propropho,propho,pho,nextpho,nenextpho,\
             prosuw,suw,nextsuw,proacc,acc,nextacc):
    #time_maneger
    startspan=3100000
    span=650000
    time1=pretime
    if pretime==0:
        time2=time1+startspan
    else:
        time2=time1+span
        
    #A_maneger_モーラ位置把握
    #A1:アクセント位置(-スタート)
    #A2:前から数えたモーラ位置
    #A3:後ろから数えたモーラ位置
    if acc!="xx":
        A1=int(acc.split("~")[1])-int(acc.split("~")[2])
        A2=int(acc.split("~")[1])
        A3=accmora[int(acc.split("~")[0])]-A2+1
    else:
        A1="xx"
        A2="xx"
        A3="xx"

    with open ("Mecabespresso/split.txt","r",encoding = "UTF-8") as f:
        line = f.readlines()

    #B_maneger_一つ前の単語品詞情報
    #B1:品詞分類(ex.動詞)
    #B2:活用形(ex.未然形)
    #B3:活用型(ex.サ変)
    if prosuw!="xx":
        B1=HTSDictionary.posDic(Mecabespresso.pos1(line[int(prosuw)]),Mecabespresso.pos2(line[int(prosuw)]),Mecabespresso.pos3(line[int(prosuw)]))
        B2=HTSDictionary.cFormDic(Mecabespresso.cForm(line[int(prosuw)]))
        B3=HTSDictionary.cTypeDic(Mecabespresso.cType(line[int(prosuw)]))
    else:
        B1="xx"
        B2="xx"
        B3="xx"

    #C_maneger_今の単語品詞情報
    #C1:品詞分類(ex.動詞)
    #C2:活用形(ex.未然形)
    #C3:活用型(ex.サ変)
    if suw!="xx":
        C1=HTSDictionary.posDic(Mecabespresso.pos1(line[int(suw)]),Mecabespresso.pos2(line[int(suw)]),Mecabespresso.pos3(line[int(suw)]))
        C2=HTSDictionary.cFormDic(Mecabespresso.cForm(line[int(suw)]))
        C3=HTSDictionary.cTypeDic(Mecabespresso.cType(line[int(suw)]))
    else:
        C1="xx"
        C2="xx"
        C3="xx"

    #D_maneger_次の単語品詞情報
    #D1:品詞分類(ex.動詞)
    #D2:活用形(ex.未然形)
    #D3:活用型(ex.サ変)
    if nextsuw!="xx":
        D1=HTSDictionary.posDic(Mecabespresso.pos1(line[int(nextsuw)]),Mecabespresso.pos2(line[int(nextsuw)]),Mecabespresso.pos3(line[int(nextsuw)]))
        D2=HTSDictionary.cFormDic(Mecabespresso.cForm(line[int(nextsuw)]))
        D3=HTSDictionary.cTypeDic(Mecabespresso.cType(line[int(nextsuw)]))
    else:
        D1="xx"
        D2="xx"
        D3="xx"

    #E_maneger_前のアクセント
    #E1:前のアクセント句のモーラ数
    #E2:前のアクセント句の核の位置
    #E3:疑問形か否か(通常:0)
    #E4:定義なし(xx)
    #E5:ポーズが入るか否か(通常:0)
    if proacc!="xx":
        E1=accmora[int(proacc.split("~")[0])]
        E2=int(proacc.split("~")[2])
        E3=0
        E4="xx"
        if pho=="pau":
            E5=1
        else:
            E5=0
    else:
        E1="xx"
        E2="xx"
        E3="xx"
        E4="xx"
        E5="xx"

    #F_maneger_今のアクセント
    #F1:今のアクセント句のモーラ数
    #F2:今のアクセント句の核の位置
    #F3:疑問形か否か(通常:0)
    #F4:定義なし(xx)
    #F5:一呼吸中で前から数えて何番目のアクセント句か
    #F6:一呼吸中で後ろから数えて何番目のアクセント句か
    #F7:一呼吸中で前から数えて何番目のモーラか
    #F8:一呼吸中で後ろから数えて何番目のモーラか
    if acc!="xx":
        F1=accmora[int(acc.split("~")[0])]
        F2=int(acc.split("~")[2])
        F3=0
        F4="xx"
        F5=int(acc.split("~")[0])+1
        F6=len(accmora)-F5+1
        for n in range(len(accmora)):
            if n!=0:
                F7=int(accmora[n-1])+int(acc.split("~")[1])
            else:
                F7=int(acc.split("~")[1])
        accall=0
        for n in range(len(accmora)):
            accall=accall+int(accmora[n])
        F8=accall-F7+1
    else:
        F1="xx"
        F2="xx"
        F3="xx"
        F4="xx"
        F5="xx"
        F6="xx"
        F7="xx"
        F8="xx"


    #G_maneger_次のアクセント
    #G1:次のアクセント句のモーラ数
    #G2:次のアクセント句の核の位置
    #G3:疑問形か否か(通常:0)
    #G4:定義なし(xx)
    #G5:ポーズが入るか否か(通常:0)
    if nextacc!="xx":
        G1=accmora[int(nextacc.split("~")[0])]
        G2=int(nextacc.split("~")[2])
        G3=0
        G4="xx"
        if nenextpho=="pau":
            G5=1
        else:
            G5=0
    else:
        G1="xx"
        G2="xx"
        G3="xx"
        G4="xx"
        G5="xx"

    #H_maneger_前の呼吸句
    #H1:前の呼吸句のアクセント句数
    H1="xx"
    #H2:前の呼吸句のモーラ数
    H2="xx"
    
    #I_maneger_今の呼吸句
    #I1:今の呼吸句のアクセント句数
    I1=len(accmora)
    #I2:今の呼吸句のモーラ数
    I2=0
    for n in range(len(accmora)):
        I2=I2+int(accmora[n])
    #I3:文章全体から数えた呼吸句(前から数えて)
    I3=1
    #I4:文章全体から数えた呼吸句(後ろから数えて)
    I4=1
    #I5:今の呼吸句中から数えたアクセント句の位置(前から数えて)
    #I6:今の呼吸句中から数えたアクセント句の位置(後ろから数えて)
    if acc!="xx":
        I5=int(acc.split("~")[0])+1
        I6=len(accmora)-I5+1
    else:
        I5="xx"
        I6="xx"
    #I7:今の呼吸句中から数えたモーラの位置(前から数えて)
    #I8:今の呼吸句中から数えたモーラの位置(後ろから数えて)
    if acc!="xx":
        for n in range(len(accmora)):
            if n!=0:
                I7=int(accmora[n-1])+int(acc.split("~")[1])
            else:
                I7=int(acc.split("~")[1])
        accall=0
        for n in range(len(accmora)):
            accall=accall+int(accmora[n])
        I8=accall-I7+1
    else:
        I7="xx"
        I8="xx"
    #J_maneger_次の呼吸句
    #J1:次の呼吸句のアクセント句数
    J1="xx"
    #J2:次の呼吸句のモーラ数
    J2="xx"

    #K_maneger_構成情報
    #K1:呼吸数でいくつか(基本的に1)
    #K2:アクセント句の数
    #K3:モーラ数
    K1=1
    K2=len(accmora)
    K3=0
    for n in range(len(accmora)):
        K3=K3+int(accmora[n])
    
    ID=str(time1)+" "+str(time2)+" "+str(propropho)+"^"+str(propho)+"-"+str(pho)+"+"+str(nextpho)+\
          "="+str(nenextpho)+"/A:"+str(A1)+"+"+str(A2)+"+"+str(A3)+"/B:"+str(B1)+"-"+str(B2)+"_"+str(B3)+\
          "/C:"+str(C1)+"_"+str(C2)+"+"+str(C3)+"/D:"+str(D1)+"+"+str(D2)+"_"+str(D3)+\
          "/E:"+str(E1)+"_"+str(E2)+"!"+str(E3)+"_"+str(E4)+"-"+str(E5)+\
          "/F:"+str(F1)+"_"+str(F2)+"#"+str(F3)+"_"+str(F4)+"@"+str(F5)+"_"+str(F6)+"|"+str(F7)+"_"+str(F8)+\
          "/G:"+str(G1)+"_"+str(G2)+"%"+str(G3)+"_"+str(G4)+"_"+str(G5)+"/H:"+str(H1)+"_"+str(H2)+\
          "/I:"+str(I1)+"-"+str(I2)+"@"+str(I3)+"+"+str(I4)+"&"+str(I5)+"-"+str(I6)+"|"+str(I7)+"+"+str(I8)+\
          "/J:"+str(J1)+"_"+str(J2)+"/K:"+str(K1)+"+"+str(K2)+"-"+str(K3)+"\n"
    with open("output/HTS_id.txt","a",encoding="UTF-8")as f:
        f.write(ID)
    return time2

def DoHTS(voice):
    subprocess.run("hts_engine -m "+voice+" -ow output/out.wav  output/HTS_id.txt",shell=True)
    
    wav_obj = simpleaudio.WaveObject.from_wave_file("output/out.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()
    return 0


def HTS(acbox,readbox,strong):
    hairetu2=MakeSuwDic()
    hairetu=AccDic(readbox,acbox)
    hairetu3=reroadByStrong(strong,hairetu[0],hairetu2[1],hairetu[1])
    hairetu4=reroadByPho(hairetu3[0],hairetu3[1],hairetu3[2])
    accmora=hairetu[2]
    phos=hairetu4[0]
    suws=hairetu4[1]
    accs=hairetu4[2]
    starttime=0
    with open("output/HTS_id.txt","w",encoding="UTF-8")as f:
        pass
    for n in range(len(phos)-4):
        accmora=accmora
        propropho=phos[n-2]
        propho=phos[n-1]
        pho=phos[n]
        nextpho=phos[n+1]
        nenextpho=phos[n+2]
        prosuw=suws[n-1]
        suw=suws[n]
        nextsuw=suws[n+1]
        proacc=accs[n-1]
        acc=accs[n]
        nextacc=accs[n+1]
        #print(accmora,propropho,propho,pho,nextpho,nenextpho,prosuw,suw,nextsuw,proacc,\
        #  acc,nextacc)
        starttime=MakeHTSID(starttime,accmora,\
        propropho,propho,pho,nextpho,nenextpho,\
        prosuw,suw,nextsuw,proacc,acc,nextacc)
    DoHTS(voice)
    return 0


#test_corner=
"""


print(HTSDictionary.moraDic("チャ"))

readbox=["フクゴー","メーシ"]
acbox=["3","1"]
print(AccDic(readbox,acbox))

"""
"""def acmake(word,strong):
    #mecabの結果から実際に抽出する
    #word="第一回目"
"""
if __name__ == "__main__":
    main()
