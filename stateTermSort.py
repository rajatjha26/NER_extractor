terms=open('stateTerms.txt','r')

dict={}

for data in terms:
    data=data.strip()
    ngram=data.split()
    dict.update({data:len(ngram)})
sortDict={k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
for key in sortDict.keys():
    print(key)