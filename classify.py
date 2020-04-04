#USAGE: python3 classify.py <query_file>
import sys
import numpy as np
from math import sqrt


def cosine_similarity(v1, v2):
    num = np.dot(v1, v2)
    den_a = np.dot(v1, v1)
    den_b = np.dot(v2, v2)
    return num / (sqrt(den_a) * sqrt(den_b))

def read_vocab():
    with open('./data/vocab_file.txt','r') as f:
        vocab = f.read().splitlines()
    return vocab

def read_queries(query_file):
    with open(query_file) as f:
        queries = f.read().splitlines()
    return queries

def read_category_vectors():
    vectors = {}
    f = open('./data/category_vectors.txt','r')
    for l in f:
        l = l.rstrip('\n')
        fields = l.split()
        cat = fields[0]
        vec = np.array([float(v) for v in fields[1:]])
        vectors[cat] = vec
    return vectors

def get_ngrams(l,n):
    l = l.lower()
    ngrams = {}
    for i in range(0,len(l)-n+1):
        ngram = l[i:i+n]
        if ngram in ngrams:
            ngrams[ngram]+=1
        else:
            ngrams[ngram]=1
    return ngrams

def normalise_tfs(tfs,total):
    for k,v in tfs.items():
        tfs[k] = v / total
    return tfs

def mk_vector(vocab,tfs):
    vec = np.zeros(len(vocab))
    for t,f in tfs.items():
        if t in vocab:
            pos = vocab.index(t)
            vec[pos] = f
    return vec

vocab = read_vocab()
print(len(vocab))
vectors = read_category_vectors()
queries = read_queries(sys.argv[1])

for q in queries:
    print("\nQUERY:",q)
    ngrams = {}
    cosines = {}
    for i in range(4,7):
        n = get_ngrams(q,i)
        ngrams = {**ngrams, **n}
    qvec = mk_vector(vocab,ngrams)
    for cat,vec in vectors.items():
        cosines[cat] = cosine_similarity(vec,qvec)
    for cat in sorted(cosines, key=cosines.get, reverse=True):
        print(cat,cosines[cat])
