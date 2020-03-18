## Part 1: document crawl

**Outcome: a dataset of web documents covering some chosen topics**


### Setting up

Clone Wikiextractor in your Wikipedia directory:

    git clone https://github.com/attardi/wikiextractor.git

Extract the wikipedia file using bunzip2:

    bunzip2 <name of wiki file>


### Getting important categories 

Run the extract_categories.py script, which will return the 50 most frequent categories for your dump file, as well as the associated page titles and external links. The relevant files will be stored in your data/ directory:

    python3 extract_categories.py enwiki-20171103-pages-articles14.xml-p7697599p7744799 

Share your category frequency file with everybody by doing a pull request (PR) to the repository. The file to share should be in your data folder, and should be called *wiki[your-file-number]_top_50_categories_freqs.txt*.

Once all PRs have been accepted, you can pull the shared data:

    git pull

Then, get a summary of the available categories:

    python3 output_top_cats.py > top_50_categories.txt

At this point, we will decide together which categories to keep. A file will be produced recording those categories only, and shared with all. For illustration purposes, let's assume that file has been called *tmp_cat.txt*.


### Extracting data for chosen categories

Extract text data for the categories in tmp_cat.txt. For this, you will need WikiExtractor:

    python WikiExtractor.py -o - --no_templates --filter_disambig_pages --filter_category <path_of_category_file> <name of wiki xml file> > <save-name>

For instance:

     python wikiextractor/WikiExtractor.py -o - --no_templates --filter_disambig_pages --filter_category tmp_cat.txt enwiki-20171103-pages-articles1.xml-p10p30302 > enwiki-20171103-pages-articles1.txt-p10p30302

At this point, you should have a clean text file containing all the articles relevant to the chosen categories. We will gather all files again to make a clean Wikipedia subcorpus, containing only the categories we are interested in.

Now, everybody should choose a category they would like to 'look after' for the rest of the practicals. Next week, everybody will receive the part of the corpus related to their chosen category.


### Feature selection

Which features should we use to generate document representations? We have seen in the course that we can use the n most frequent words in the vocabulary as features, or better, use Mutual Information. Another common way to do this in Information Retrieval is the TF-IDF measure.

Check out the definition of TF-IDF here: [https://en.wikipedia.org/wiki/Tf%E2%80%93idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). Can you explain how to use that measure in our setting, where each person is responsible for one Wikipedia category?
