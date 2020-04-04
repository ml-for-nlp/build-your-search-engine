#USAGE: python3 ngrams.py <ngram size>

import sys
from os import listdir
from os.path import isfile, isdir, join
    

d = './data/categories'
catdirs = [join(d,o) for o in listdir(d) if isdir(join(d,o))]
n = int(sys.argv[1])

for cat in catdirs:
    ngrams = {}
    f = open(join(cat,'linear.txt'),'r')
    for l in f:
        if "<doc id" not in l and "</doc" not in l:
            l = l.rstrip('\n').lower()
            for i in range(len(l)-n+1):
                ngram = l[i:i+n]
                
                if ngram in ngrams:
                    ngrams[ngram]+=1
                else:
                    ngrams[ngram]=1
    f.close()

    ngramfile = open(join(cat,"linear."+str(n)+".ngrams"),'w')
    for k in sorted(ngrams, key=ngrams.get, reverse=True):
        ngramfile.write(k+'\t'+str(ngrams[k])+'\n')
    ngramfile.close() 
