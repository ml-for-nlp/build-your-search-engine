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


## Part 2 - directing queries to topics

By now, we should have k categories (corresponding to the work of k students), and the raw Wikipedia text corresponding to those categories, as output by WikiExtractor. The raw text will be stored in different folder of the *data/categories* directory, under a file called *linear.txt*.

Our next goal is to see how we can map incoming search queries to each category. The point of this is that, as our search engine grows (to potentially millions, or billions of pages), it would be very inefficient to try and find the answer to a movie-related query in our "gecko and other lizards" category. We want to narrow things down.

The repository now contains scripts to compute character ngram frequencies for each category. You can run it doing:

    python3 ngrams.py [ngram-size]

For instance,

    python3 ngrams.py 6

will create a file in each subfolder of *data/categories*, showing a sorted list of ngrams of size 6.

We probably want several ngram sizes. So re-run the script for size 4-6, for instance.

Next, we will want to compute the td-idf of each ngram in each category. You can do this by running:

    python3 output_top_tfidf_ngrams.py

This will create a *tf_idfs.txt* file in each category subfolder. In addition, the script captures the 100 ngrams with highest tf-idf *for each category* and uses them to generate a set of features, saved in the file *data/vocab.txt*. In essence, what we are doing here is simple feature selection, based on the highest-ranked ngrams across categories.

Now that we have our features, we can build vector representations for each category. If we have ended up with, say, 1500 features in our feature selection step, we will build 1500-dimensional vectors to represent each category, with each component of a vector set to the tf-idf of the relevant dimensions for that category. As an example, if *actor* is the 16th dimension in our 1500-dimensional space, and category *russian_language_films* has a tf-idf of 1.147e-05 for that ngram, then dimension 16 will be set to that number in the *russian_language_film* vector.

You can create your category vectors with

    python3 mk_cat_vectors.py

And now... finally. The test! The file *query_file.txt* contains a set of queries (massaged to match the 2020 categories you have extracted!) You can add to that file, one query per line. We want to see whether the system finds the right category for each query. Run the following:

    python3 classify.py query_file.txt

and you will return a ranked list of categories for each query. You of course want to most relevant categories at the top.

Play with the *classify.py* script, and with adding queries to the file. What works, what doesn't? Why?
