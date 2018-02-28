import json
from sys import argv
import sys


tran_pro={}
emis_pro={}
word_list={}


#=============================================

def load_model():
    ifp = open("hmmmodel.txt")
    fileList = ifp.readlines()
    global tran_pro
    tran_pro = json.loads(fileList[0])
    global emis_pro
    emis_pro = json.loads(fileList[1])
    global word_list
    word_list = json.loads(fileList[2])


#=============================================

def viterbi(sent):
    word=sent.split(" ")
    state_num=tran_pro.__sizeof__()
    tag_list = []
    for key in tran_pro.keys():
        for tag in tran_pro[key].keys():
            if tag in tag_list:
                continue
            else:
                tag_list.append(tag)

    start_pro = tran_pro["-SSSS-"]

    matrix = [[0]*len(word) for i in range(len(tag_list))]
    backtrak = [[0]*len(word) for i in range(len(tag_list))]
    # initial first word
    for tag in start_pro.keys():

        if tag in tag_list:
            tag_index=tag_list.index(tag)
            matrix[tag_index][0]=start_pro[tag]*get_emis_pro(word[0],tag)





    # viterbi

    for index in range(len(word)-1):
        for tag_index_cur in range(len(tag_list)):
            max_a=0
            back_index=0;
            for tag_index_pre in range(len(tag_list)):
                #matrix[tag_index_cur][index+1]=max(
               #     matrix[tag_index_pre][index]*get_tran_pro(tag_list[tag_index_pre],tag_list[tag_index_cur])*get_emis_pro(word[index+1],tag_list[tag_index_cur]),
               #     matrix[tag_index_cur][index+1]
               # )
                temp = matrix[tag_index_pre][index]*get_tran_pro(tag_list[tag_index_pre],tag_list[tag_index_cur])
                if temp> max_a:
                    max_a=temp
                    back_index=tag_index_pre
                #print(word[index+1] + "->" + tag + ":")
            matrix[tag_index_cur][index+1]=max_a*get_emis_pro(word[index+1],tag_list[tag_index_cur])
            backtrak[tag_index_cur][index+1]=back_index
    max_res=0
    last_index=0
    res=[]
    for index in range(len(matrix)):
        if matrix[index][-1]>max_res:
            max_res=matrix[index][len(matrix[0])-1]
            last_index=index

    i=len(backtrak[0])-1
    j = last_index
    while(i>=0):
        res.append(tag_list[j])
        j=backtrak[j][i]
        i-=1

    res.reverse()
    #print(res)
    tagged_sent=""
    for index in range(len(word)):
        tagged_sent+=word[index]+"/"+res[index]+" "
    return tagged_sent

#=============================================
def get_emis_pro(word,tag):


    res=0.0
    if (word not in word_list.keys()) and tag=="NN":
        return 0.000000001
    if word.startswith("http://www.") and tag=="ADD":
        return 1
    if tag in emis_pro.keys():

        if word in emis_pro[tag].keys():
            res= emis_pro[tag][word]
    if tag == "NNP" and res == 0:
        res += 0.001
    return res


#=============================================

def get_tran_pro(pre,cur):
    res = 0
    if pre in tran_pro.keys():
        if cur in tran_pro[pre].keys():
            res=tran_pro[pre][cur]
    return res

#=============================================


def pred_test(path):
    ifp=open(path)
    ofp=open("hmmoutput.txt","w")
    fileList=ifp.readlines()
    for raw in fileList:
        line=raw.splitlines()
        sent=line[0]
        tagged_sent=viterbi(sent)
        ofp.write(tagged_sent)
        ofp.write("\n")
    ifp.close()
    ofp.close()


#=============================================


if __name__ == '__main__':

    load_model()
    #pred_test(argv)
    #print(viterbi("fat people eat accumulates"))
    pred_test("coding1-data-corpus/en_dev_raw.txt")
