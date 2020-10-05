import re
from nltk.tokenize import sent_tokenize 
from stanza.server import CoreNLPClient
import time

pronoun=["i","you","he","she","it","they","me","him","her","it","my","mine","your","yours","his","her","hers","its","who","whom","whose","what","which","another", "each","everything","nobody","either","someone","that","myself","yourself","himself","herself","itself","this"]
nerFile=open("Functional_foods_NerData.txt","w")
finalNer=[]
filename=open("Statename.txt",'r')
for files in filename:
    files=re.sub(r"\n","",files)
    f=open(files,'r')
    allData=""
    for data in f:
        allData=allData+data
    allData=re.sub(r"(\s)*\n(\n)*(\s)*","\n",allData)
    allData=re.sub(r"(\.)*\n",".\n",allData)
    nerCollector=[]
    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner', 'parse'],
            timeout=500000,
            memory='8G') as client:
        ann = client.annotate(allData)
        for sentence in ann.sentence:
            for data in sentence.mentions:
                if(data.ner=="LOCATION" or data.ner=="ORGANIZATION" or data.ner=="PERSON" or data.ner=="STATE_OR_PROVINCE" or data.ner=="COUNTRY" or data.ner=="COUNTRY" or data.ner=="CITY"):
                    nerdata=data.entityMentionText
                    nerdata=nerdata.lower()
                    if(nerdata not in finalNer and nerdata not in pronoun):
                        nerCollector.append(nerdata)
                        finalNer.append(nerdata)
    for ners in nerCollector:
        print(ners)
for ners in finalNer:
        nerFile.write(ners)
        nerFile.write("\n")
