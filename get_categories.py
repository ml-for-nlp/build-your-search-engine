#!/usr/bin/python3

"""
    get_allcategories.py

    MediaWiki API Demos
    Demo of `Allcategories` module: Get all categories, starting from a
    certain point, as ordered by category title.

    MIT License
"""

import requests
import re

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "list": "allcategories",
    "acmin": 200,
    "aclimit": 500
}

for i in range(100):
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    CATEGORIES = DATA["query"]["allcategories"]

    for cat in CATEGORIES:
        cat_name = cat["*"]
        m = re.search("[0-9]{4}",cat_name)
        #if cat_name[-6:] not in ['births','deaths']:
        if not m:
            print(cat_name)
    
    if "continue" in DATA:
        PARAMS["acfrom"] = DATA["continue"]["accontinue"]
    else:
        break
