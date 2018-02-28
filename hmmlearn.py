import os
import json
import sys
from sys import argv

word_dict={}
tag_transit={}
tran_pro={}
emis_pro={}
word_list={}
#=============================================

def precess_data(input_str):
    ifp = open(input_str)
    fileList = ifp.readlines()
    for line in fileList:

        raw=line.splitlines()
        raw[0]="-SSSS-/-SSSS- "+raw[0]
        pair = raw[0].split(" ")

        for index in range(len(pair)-1):
            word_tagger_cur = os.path.split(pair[index])
            word_tagger_next = os.path.split(pair[index+1])
            if word_tagger_cur[1] in tag_transit:
                if word_tagger_next[1] in tag_transit[word_tagger_cur[1]]:
                    tag_transit[word_tagger_cur[1]][word_tagger_next[1]]=tag_transit[word_tagger_cur[1]][word_tagger_next[1]]+1;
                else:
                    tag_transit[word_tagger_cur[1]][word_tagger_next[1]]=1
            else:
                tag_transit[word_tagger_cur[1]]={word_tagger_next[1]:1}

        for tagged in pair:
            word_tagger = os.path.split(tagged)
            #if word_tagger[1].endswith("\n"):
                #print(word_tagger[1])
                #word_tagger[1] = word_tagger[1]
            if word_tagger[1] in word_dict:
                if word_tagger[0] in word_dict[word_tagger[1]]:
                    word_dict[word_tagger[1]][word_tagger[0]] = word_dict[word_tagger[1]][word_tagger[0]] + 1
                else:
                    word_dict[word_tagger[1]][word_tagger[0]] = 1
            else:
                word_dict[word_tagger[1]] = {word_tagger[0]:1}
    ifp.close()



    for temp in tag_transit.keys():
        total = 0
        for tagger in tag_transit[temp].items():
            total += int(tagger[1])
        for tagger in tag_transit[temp].items():
            if temp in tran_pro:

                tran_pro[temp][tagger[0]] = float(tagger[1] / total)
            else:
                tran_pro[temp] = {tagger[0]: float(tagger[1] / total)}
    for temp in word_dict.keys():
        total = 0
        for tagger in word_dict[temp].items():
            if tagger[0] not in word_list.keys():
                word_list[tagger[0]]=1
            total += int(tagger[1])
        for tagger in word_dict[temp].items():
            if temp in emis_pro:

                emis_pro[temp][tagger[0]] = float(tagger[1] / total)
            else:
                emis_pro[temp]={tagger[0]:float(tagger[1] / total)}

    model = json.dumps(tran_pro)
    ofp = open("hmmmodel.txt",'w')
    ofp.writelines(model)
    ofp.write("\n")
    model = json.dumps(emis_pro)
    ofp.writelines(model)
    ofp.write("\n")
    model = json.dumps(word_list)
    ofp.writelines(model)
    ofp.write("\n")
    ofp.close()

#=============================================

if __name__ == '__main__':
    #precess_data(argv[1])
    precess_data("coding1-data-corpus/en_train_tagged.txt")