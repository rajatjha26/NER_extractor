from nltk.tree import *
import re

# strs="(ROOT (S (S (NP (PRP She)) (VP (VBD completed) (NP (PRP$ her) (NN literature) (NN review)))) (, ,) (CC but) (S (NP (PRP she)) (ADVP (RB still)) (VP (VBZ needs) (S (VP (TO to) (VP (VB work) (PP (IN on) (NP (PRP$ her) (NNS methods) (NN section))) (SBAR (RB even) (IN though) (S (NP (PRP she)) (VP (VBD finished) (NP (PRP$ her) (NNS methods) (NN course)) (NP (JJ last) (NN semester)))))))))) (. .)))"
strs="(ROOT (S (S (NP (PRP She)) (VP (VBD completed) (NP (PRP$ her) (NN literature) (NN review)))) (, ,) (CC but) (S (S (NP (PRP she)) (ADVP (RB still)) (VP (VBZ needs) (S (VP (TO to) (VP (VB work) (PP (IN on) (NP (PRP$ her) (NNS methods) (NN section))) (SBAR (RB even) (IN though) (S (NP (PRP she)) (VP (VBD finished) (NP (PRP$ her) (NNS methods) (NN course)) (NP (JJ last) (NN semester)))))))))) (CC and) (S (NP (PRP he)) (ADVP (RB carefully)) (VP (VBD followed) (NP (DT the) (JJ MEAL) (NN plan)) (PP (IN for) (NP (NN organization)))))) (. .)))"

def breakCC(str1,break_using):
    data=re.sub(r"\n|[\s][\s]+"," ",str1)
    ptree=ParentedTree.fromstring(data.strip())
    sepCC=[]
    for j in ptree.subtrees(filter=lambda x: x.label()==break_using):
        if(j.parent().label()=="S" or j.parent().label()=="SBAR"):
            temp=[]
            k=j
            while(k.left_sibling()):
                # print(k.left_sibling().pretty_print())
                k=k.left_sibling()
                p=0
                for s in k.subtrees(filter=lambda x: x.label()==break_using):
                    if(s.parent().label()=="S" or s.parent().label()=="SBAR"):
                        p=1
                        break
                if(p==0):
                    temp.append(str(k))
            temp.reverse()
            for i in temp:
                sepCC.append(i)
            sepCC.append(str(j))

            k=j
            while(k.right_sibling()):
                k=k.right_sibling()
                p=0
                for s in k.subtrees(filter=lambda x: x.label()=='CC'):
                    if(s.parent().label()=="S" or s.parent().label()=="SBAR"):
                        p=1
                        break
                if(p==0):
                    sepCC.append(str(k))
    if(len(sepCC)==0):
        sepCC.append(str1)
    return sepCC

res=[]
strss="(ROOT (S (S (PP (IN With) (NP (NP (NN pizza) (CC and) (NN soda)) (PP (IN at) (NP (NN hand))))) (, ,) (NP (PRP they)) (VP (VBD studied) (NP (NNP APA) (NNS rules)) (PP (IN for) (NP (JJ many) (NNS hours))))) (, ,) (CC and) (S (NP (PRP they)) (VP (VBD decided) (SBAR (IN that) (S (S (VP (VBG writing) (PP (IN in) (NP (NNP APA))))) (VP (VBD made) (NP (NN sense)) (SBAR (IN because) (S (NP (PRP it)) (VP (VBD was) (ADJP (JJ clear) (, ,) (JJ concise) (, ,) (CC and) (JJ objective)))))))))) (. .)))"
arr1=breakCC(strss,"CC")
for data in arr1:
    res.append(breakCC(data,":"))
final_out=[]
for i in res:
    for j in i:
        data=re.sub(r"\n|[\s][\s]+"," ",j)
        data=data.strip()
        final_out.append(data)
for i in final_out:
    print(i)
