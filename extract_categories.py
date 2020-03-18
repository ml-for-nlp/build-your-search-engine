# Returns 50 most frequent categories from wikipedia xml dump file, with associated titles

import re
import sys
import os

def extract_links(out):
    m = re.findall("cite web \|url=(http[^\|]*)",out)
    return m

if not os.path.exists('./data'):
    os.makedirs('./data')

f = open(sys.argv[1],'r')
m = re.search("articles([0-9]*)\.",sys.argv[1])
wiki_id = m.group(1)
    
categories = {}
titles = {}
links = {}
title = ""
current_links = []

for l in f:
    if "<title>" in l:
        m = re.search(r'<title>(.*)<',l)
        title=m.group(1) 
        title=title.replace(' ','_')
        current_links = []
    tmp_links = extract_links(l)
    if tmp_links != []:
        current_links.extend(tmp_links)
    m = re.search("\[\[Category:(.*)\]\]",l)
    if m and title !="":
        cat = m.group(1)
        if cat in categories:
            categories[cat]+=1
            titles[cat].append(title)
            links[cat].extend(current_links)
        else:
            categories[cat]=1
            titles[cat] = [title]
            links[cat] = current_links
f.close()

cat_file = open("data/wiki"+wiki_id+"_top_50_categories_freqs.txt",'w')
title_file = open("data/wiki"+wiki_id+"_top_50_categories_titles.txt",'w')
link_file = open("data/wiki"+wiki_id+"_top_50_categories_links.txt",'w')

for k in sorted(categories, key=categories.get, reverse=True)[:100]:
    cat_file.write(k+'\t'+str(categories[k])+'\n')
    title_file.write(k+'\t'+','.join(t for t in titles[k])+'\n')
    link_file.write(k+'\t'+','.join(l for l in links[k])+'\n')

cat_file.close()
title_file.close()
link_file.close()
