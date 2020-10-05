from nltk import pos_tag
from nltk.tree import *
import re


def removeDT(parse):
    mainLeaves=parse.leaves()
    DT=[]
    PRP=[]
    PRPdOller=[]
    withoutDTPRP=[]
    for i in  parse.subtrees(filter=lambda x: x.label()=="DT"):
        DT=i.leaves()
    for i in  parse.subtrees(filter=lambda x: x.label()=="PRP"):
        PRP=i.leaves()
    for i in  parse.subtrees(filter=lambda x: x.label()=="PRP$"):
        PRPdOller=i.leaves()    
    if(len(DT)==0 and len(PRP)==0 and len(PRPdOller)==0):
        return mainLeaves



verb=["VB","VBD","VBG","VBN","VBP","VBZ"]

regex = r"(^(((JJ|JJR|JJS)|(NN|NNP|NNS|NNPS)|\s)*((NN|NNP|NNS|NNPS)\s(IN))? ((JJ|JJR|JJS|HYPH)|(NN|NNP|NNS|NNPS)|\s)*(NN|NNP|NNS|NNPS))$)"

fileinp=open("parseProcessed.txt","r")
out=[]
for parseOut in fileinp:
    ptree=ParentedTree.fromstring(parseOut)
    npArray=[]
    dict={}
    poslist=pos_tag(ptree.leaves())
    for i in poslist:
        dict.update({i[0]:i[1]})
    
    for i in  ptree.subtrees(filter=lambda x: x.label()=='NP'):
        if i not in npArray:
            npArray.append(i)

    for i in npArray:
        pos=""
        leaf=i.leaves()
        for data in leaf:
            data=data.strip()
            pos=pos+" "+dict[data]
        pos=pos.strip()
        pos=re.sub(r"^(DT|PRP|PRP$)\s","",pos)
        if(re.search(regex, pos)):
            parse=removeDT(i)
            if(parse):
                res=parse[0]
                for k in parse[1::1]:
                    res=res+" "+k.strip()
                    res=res.lower()
                if(res not in out):
                    print(res)
                    out.append(res)
                    # print(i)
