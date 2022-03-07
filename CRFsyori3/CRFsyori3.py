# -*- coding: utf-8 -*-
#CRFで予測したアクセント句の強調可能性()
#unidicの品詞を用いた予測
import subprocess

"""
1.CRF予測を格納する
"""
#CRF予測を格納する==============================================
def CRFbox(SUW,pos,Type,Form,poss,kana):
    
    #test data maker
    with open ("CRFsyori3/test.txt","w",encoding="UTF-8")as f:
        for n in range(len(SUW)):
            f.write(SUW[n]+"\t"+SUW[n]+","+pos[n]+","+Type[n]+","+Form[n]+","+poss[n]+","+kana[n]+"\n")
        f.write("EOS\tEOS\n")
    #run by CRF
    subprocess.run("crf_test -m CRFsyori3/model_file CRFsyori3/test.txt >CRFsyori3/result.txt",shell=True)
    #read results
    with open ("CRFsyori3/result.txt","r",encoding="UTF-8")as f:
        lines=f.readlines()
        box=[]
        for n in range(len(lines)):
            lines[n]=lines[n].split()
            if lines[n][0]=="EOS":
                break
            box.append(lines[n][2])
    return box



#test
#print(CRFbox(["三","回"]))

if __name__ == "__main__":
    main()


