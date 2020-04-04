#USAGE: python3 mk_cat_vectors.py

import sys
import numpy as np
from os import listdir
from os.path import isfile, isdir, join
    

def read_vocab2():
    i_to_ngrams = {}
    ngrams_to_i = {}
    c = 0
    f = open('./data/vocab_file.txt','r')
    for l in f:
        l = l.rstrip()
        i_to_ngrams[c] = l
        ngrams_to_i = c
        c+=1
    return i_to_ngrams, ngrams_to_i

def read_vocab():
    with open('./data/vocab_file.txt','r') as f:
        vocab = f.read().splitlines()
    return vocab

d = './data/categories'
catdirs = [join(d,o) for o in listdir(d) if isdir(join(d,o))]
vocab = read_vocab()
vector_file = open('./data/category_vectors.txt','w')

for cat in catdirs:
    print(cat)
    vec = np.zeros(len(vocab))
    f = open(join(cat,'tf_idfs.txt'),'r')
    for l in f:
        l = l.rstrip('\n')
        ngram = ' '.join([i for i in l.split()[:-1]])
        tf_idf = float(l.split()[-1])
        pos = vocab.index(ngram)
        vec[pos] = tf_idf
    f.close()

    vector_file.write(cat+' '+' '.join([str(v) for v in vec])+'\n')
vector_file.close()
