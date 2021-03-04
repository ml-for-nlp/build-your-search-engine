#!/usr/bin/python3

import requests
import os

def read_categories():
    with open("tmp_cat.txt",'r') as f:
        categories = f.read().splitlines()
    return categories






S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

categories = read_categories()
print(categories)


for cat in categories:
    cat_dir = "data/categories/"+cat.replace(' ','_')
    if not os.path.isdir(cat_dir):
        os.mkdir(cat_dir)
    title_file = open(os.path.join(cat_dir,"titles.txt"),'w')

    PARAMS = {
        "action": "query",
        "list": "categorymembers",
        "format": "json",
        "cmtitle": "Category:"+cat,
        "cmlimit": "100"
    }

    for i in range(1):    #increase 1 to more to get additional data
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA["query"]["categorymembers"]

        for page in PAGES:
            title = page["title"]
            ID = str(page["pageid"])
            if title[:9] != "Category:":
                title_file.write(ID+' '+title+'\n')
 
        if "continue" in DATA:
            PARAMS["cmcontinue"] = DATA["continue"]["cmcontinue"]
        else:
            break

    title_file.close()
