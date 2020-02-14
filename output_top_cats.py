import sys
from os import listdir
from os.path import isfile, join

dir_files = [f for f in listdir('./data') if isfile(join('./data', f)) and 'categories_freqs' in f]

summary_categories = {}
for filename in dir_files:
    #print("Processing",filename,"...")
    cat_file = open(join('./data',filename),'r')
    for l in cat_file:
        cat = l.rstrip('\n').split('\t')[0]
        num = int(l.rstrip('\n').split('\t')[1])
        if cat in summary_categories:
            summary_categories[cat]+=num
        else:
            summary_categories[cat]=num
    cat_file.close()

for k in sorted(summary_categories, key=summary_categories.get, reverse=True)[:50]:
    #print(k+'\t'+str(summary_categories[k]))
    print(k)
 


