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

    
    for i in mainLeaves:
        if i in DT:
            continue
        if i in PRP:
            continue
        if i in PRPdOller:
            continue
        withoutDTPRP.append(i)
    return withoutDTPRP    






def result(inp_file):
    f=open(inp_file,"r")
    outfile=open("termsParsed.txt","w")
    outterms=open("terms.txt","w")
    # PrintLog("Generating Parse Tree")
    for parse_data in f:
        if(parse_data.strip()==""):
            continue
        parse_data=parse_data.strip()
        ptree1=ParentedTree.fromstring(parse_data)
        npArray=[]
        for i in  ptree1.subtrees(filter=lambda x: x.label()=='NP'):
            j=""
            for j in  i.subtrees(filter=lambda x: x.label()=='NP'):
                continue
            if j not in npArray:
                npArray.append(j)
        
        out=[]
        for np in npArray:
            notUnigram=np.leaves()
            if(len(notUnigram)>1):
                parse=removeDT(np)
                if(len(parse)>1):
                    outfile.write(str(np))
                    outfile.write("\n")
                    res=parse[0]
                    for k in parse[1::1]:
                        res=res+" "+k
                        res=res.lower()
                    if(res not in out):
                        outterms.write(res)
                        outterms.write("\n")
                        out.append(res)






def start():
    input_file=""
    try:
        options, _ = getopt.getopt(sys.argv[1:], 'hi:',['ifile=','help',])
    except getopt.GetoptError:
        print ('nounPhaseIdent.py -i <inputfile>')
        sys.exit(2)

    
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print("Usage: \
                \n -i --input file, \
                \n -h, --help")
            print('coammand: \
            \n nounPhaseIdent.py -i <inputfile>"')
            sys.exit(1)	
        elif opt in ('-i', '--ifile'):
            input_file = arg
            # PrintLog('input file=%s'%arg)
    if(not input_file):
        print("nounPhaseIdent.py -i <inputfile>")
        sys.exit(2)
    result(input_file)

start()