import sys
import os
from os import listdir
from os.path import isfile, join

def read_categories(filename):
    with open(filename) as f:
        cats = f.read().splitlines() 
    return cats

def create_directory(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def write_titles(titles,cat):
    cat_dir = cat.replace(' ','_')
    f = open(join(join('./data',cat_dir),'titles.txt'),'w')
    for title in titles:
        f.write(title+'\n')
    f.close()    

def summarise_titles(cat):
    all_titles = []
    dir_files = [f for f in listdir('./data') if isfile(join('./data', f)) and 'categories_titles' in f]
    for f in dir_files:
       cat_titles = open(join('./data',f))
       for l in cat_titles:
           fields = l.rstrip('\n').split('\t')
           c = fields[0]
           titles = fields[1]
           if c == cat:
               all_titles.extend(titles.split(','))       
               break
    write_titles(all_titles,cat)

cats = read_categories(sys.argv[1])
for cat in cats:
    catdir = cat.replace(' ','_')
    create_directory(join('./data',catdir))
    summarise_titles(cat)
