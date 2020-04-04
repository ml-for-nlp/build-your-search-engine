import sys
import string
from math import log
from os import listdir
from os.path import isfile, isdir, join


d = './data/categories'
catdirs = [join(d,o) for o in listdir(d) if isdir(join(d,o))]

def contain_punctuation(s):
    punctuation = [c for c in string.punctuation]
    punctuation.append(' ')
    r = any(c in s for c in punctuation) 
    return r

def normalise_tfs(tfs,total):
    for k,v in tfs.items():
        tfs[k] = v / total
    return tfs

def log_idfs(idfs,num_cats):
    for k,v in idfs.items():
        idfs[k] = log(num_cats / v)
    return idfs

cat_tfs = {}
cat_tf_idfs = {}
idfs = {}

for cat in catdirs:
    print(cat)
    tfs = {}
    sum_freqs = 0
    #print("Processing",filename,"...")
    ngram_files = [join(cat,f) for f in listdir(cat) if isfile(join(cat, f)) and '.ngrams' in f]
    for ngram_file in ngram_files:
        f = open(ngram_file,'r')
        for l in f:
            l = l.rstrip()
            ngram = '\t'.join(i for i in l.split('\t')[:-1])
            freq = int(l.split('\t')[-1])
            tfs[ngram] = freq
            sum_freqs+=freq
            if ngram in idfs:
                idfs[ngram]+=1
            else:
                idfs[ngram]=1
        f.close()

    tfs = normalise_tfs(tfs,sum_freqs)
    cat_tfs[cat] = tfs

    #for k in sorted(idfs, key=tfs.get, reverse=True)[:10]:
    #    print(k,idfs[k])

idfs = log_idfs(idfs, len(catdirs))

vocab=[]

for cat in catdirs:
    tf_idfs = {}
    tfs = cat_tfs[cat]
    for ngram,tf in tfs.items():
        tf_idfs[ngram] = tf * idfs[ngram]
    cat_tf_idfs[cat] = tf_idfs

    c = 0
    for k in sorted(tf_idfs, key=tf_idfs.get, reverse=True):
        #only keep top 100 dimensions per category. Also, we won't keep ngrams with spaces
        if c == 100:
            break
        if k not in vocab and not contain_punctuation(k):
            vocab.append(k)
            c+=1

print("VOCAB SIZE:",len(vocab))

#Write tf-idfs for each category
for cat in catdirs:
    tf_idfs = cat_tf_idfs[cat]
    f = open(join(cat,'tf_idfs.txt'),'w')
    for ngram in sorted(vocab):
        if ngram in tf_idfs:
            f.write(ngram+' '+str(tf_idfs[ngram])+'\n')
        else:
            f.write(ngram+' 0.0\n')
    f.close()
 

vocab_file = open("./data/vocab_file.txt",'w')
for ngram in sorted(vocab):
    vocab_file.write(ngram+'\n')
vocab_file.close()

