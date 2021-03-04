#!/usr/bin/python3

import requests
import os

def read_titles(filename):
    IDs = []
    titles = []
    f = open(filename,'r')
    for l in f:
        l.rstrip('\n')
        IDs.append(l.split()[0])
        titles.append(' '.join(l.split()[1:]))
    return IDs,titles


def read_categories():
    with open("tmp_cat.txt",'r') as f:
        categories = f.read().splitlines()
    return categories



S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"


categories = read_categories()

for cat in categories:
    print("Processing category".cat)
    cat_dir = "data/categories/"+cat.replace(' ','_')
    title_file = os.path.join(cat_dir,"titles.txt")
    IDs, titles = read_titles(title_file)

    content_file = open(os.path.join(cat_dir,"linear.txt"),'w')

    for i in range(len(titles)):
        PARAMS = {
            "action": "query",
            "prop": "extracts",
            "format": "json",
            "exintro": True,
            "explaintext": True,
            "redirects": True,
            "titles": titles[i]
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA["query"]["pages"]

        for page in PAGES:
            extract = PAGES[page]["extract"]
            content_file.write("<doc id=\""+IDs[i]+"\" title=\""+titles[i]+"\">\n")
            content_file.write(extract+'\n')
            content_file.write("</doc>\n\n")

    content_file.close()
