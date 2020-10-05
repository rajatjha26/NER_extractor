from nltk import *
import getopt
import sys
import inspect
import re


def PrintLog(message="Here....."):
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                                # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print ("LOG: %s:, %s:, %s:, %s" %(info.filename, info.function, info.lineno, message))

def breakCC(str1,break_using):
    data=re.sub(r"\n|[\s][\s]+"," ",str1)
    ptree=ParentedTree.fromstring(data.strip())
    sepCC=[]
    for j in ptree.subtrees(filter=lambda x: x.label()==break_using):
        if(j.parent().label()=="S" or j.parent().label()=="SBAR"):
            temp=[]
            k=j
            while(k.left_sibling()):
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

def result(inp_file):
    f=open(inp_file,"r")
    outfile=open("result.txt","w")
    PrintLog("Generating Parse Tree")
    for parse_data in f:
        if(parse_data.strip()==""):
            continue
        ptree=ParentedTree.fromstring(str(parse_data))
        outfile.write("Sentence: ")
        inputChunk=ptree.leaves()
        inputSentence=inputChunk[0].strip()
        for data in inputChunk[1::1]:
            if(data not in[",",".","!","?","-","'"]):
                inputSentence=inputSentence+" "+str(data.strip())
            else:
                inputSentence=inputSentence+str(data.strip())
        outfile.write(inputSentence)
        outfile.write("\n")
        res=[]
        arr1=breakCC(parse_data,"CC")
        for data in arr1:
            res.append(breakCC(data,":"))
        final_out=[]
        for i in res:
            for j in i:
                data=re.sub(r"\n|[\s][\s]+"," ",j)
                data=data.strip()
                final_out.append(data)       
        a=[]
        for breakstr in final_out:
            sent=[]
            ptree1=ParentedTree.fromstring(breakstr)
            inputChunk=ptree1.leaves()
            ptree1Sent=inputChunk[0].strip()
            for data in inputChunk[1::1]:
                if(data not in[",",".","!","?","-","'"]):
                    ptree1Sent=ptree1Sent+" "+str(data.strip())
                else:
                    ptree1Sent=ptree1Sent+str(data.strip())
            for i in  ptree1.subtrees(filter=lambda x: x.label()=='SBAR'):
                string=i.leaves()
                sentence_chunk=str(string[0].strip())
                for word in string[1::1]:
                    word=word.strip()
                    if(word not in[",",".","!","?","-","'"]):
                        sentence_chunk=sentence_chunk+" "+str(word)
                    else:
                        sentence_chunk=sentence_chunk+str(word)
                sent.append(sentence_chunk)
            for part in sent:
                ptree1Sent=ptree1Sent.replace(part,"")
            a.append(ptree1Sent.strip())

            for part in range(len(sent)):
                tempSt=sent[part]
                for rec in range(part+1,len(sent)):
                    tempSt=tempSt.replace(sent[rec],"")
                a.append(tempSt.strip())
        sentenceInSeq=[]
        lengthOfSentSpace=len(a)
        sent1=""
        for i in range(len(a)):
            if(i<len(a)-1):
                if(len(a[i])>1 and len(a[i+1])>1):
                    outfile.write(a[i])
                    outfile.write("\n")
                elif(len(a[i])==1):
                    sent1=sent1+a[i]
                    outfile.write(sent1)
                    outfile.write("\n")
                else:
                    sent1=a[i]
            else:
                if(len(a[i])>1):
                    outfile.write(a[i])
                    outfile.write("\n")
                else:
                    sent1=sent1+a[i]
                    outfile.write(sent1)
                    outfile.write("\n")
        outfile.write("\n")

    PrintLog("output file result.txt is created.\nDone.")

def start():
    input_file=""
    try:
        options, _ = getopt.getopt(sys.argv[1:], 'hi:',['ifile=','help',])
    except getopt.GetoptError:
        print ('result.py -i <inputfile>')
        sys.exit(2)

    
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print("Usage: \
                \n -i --input file, \
                \n -h, --help")
            print('coammand: \
            \n result.py -i <inputfile>"')
            sys.exit(1)	
        elif opt in ('-i', '--ifile'):
            input_file = arg
            PrintLog('input file=%s'%arg)
    if(not input_file):
        print("result.py -i <inputfile>")
        sys.exit(2)
    result(input_file)

start()