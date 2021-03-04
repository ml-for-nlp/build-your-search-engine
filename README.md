# Document classification for Web search

The basis of a search engine is a collection of documents converted to a machine-readable representation, and classified into broad topics. Imagine doing search on a small set of 1M documents. You might have 100K documents in *computer science* topic, 100K in the *animals* topic, another 100K in a *politics* topic, etc. When a user query comes in, say *How do I learn Python?*, you ideally want to classify the query into the *computer science* topic, so that you only have to search through 100K documents rather than the whole 1M document collection.

In this practical, we will use Wikipedia to create a small collection of documents on certain topics. We will convert those documents into vectors. And finally, we will test whether a given user query is mapped to the correct topic in the collection.


## Part 1 - gathering some data


### Wikipedia category processing


We will first retrieve a number of topics from the Wikipedia category tree. We will use the [Wikimedia API](https://www.mediawiki.org/wiki/API:Main_page) for this:

   python3 get_categories.py > wiki_categories.txt

The code returns all Wikipedia categories for which at least 200 documents exist.

In case you have difficulties running the code, you will find an already processed list in the data folder: *data/preprocessed_wiki_categories.txt*.

Open your *wiki_categories.txt* file and scroll through it. Select 10 categories from it. Make sure you don't select categories which look like Wikipedia-internal labels (e.g. `Wikipedia books', `Pages with script errors', etc). Copy and paste those category names into a file named *tmp_cat.txt*. For instance, you might end up with the following:

    Brazilian telenovelas
    Cold War films
    Fauna of Zimbabwe
    Freeware games
    International law
    Landscape painters
    Members of the Chinese Academy of Sciences
    Musicals based on novels
    Particle physics
    21st-century women mathematicians


### Wikipedia page crawl

We will now retrieve Wikipedia pages for our categories. We first need a list of page titles for each category. To do so, we will use the API again and run the following:

    python3 get_category_pages.py

This will create a file *titles.txt* for each category in your *data/* directory, containing 100 Wikipedia titles for each of the categories in your *tmp_cat.txt* file. We now need to retrieve the text of those documents. To speed things up and in order not to use too much hard disk space, we will just retrieve the intro text of each document rather than the whole page. Run:

    python3 get_page_content.py

This will create a file *linear.txt* for each category in your *data/* directory, containing the introductory text of each Wikipedia page listed in *titles.txt* files. The calls to the Wikipedia API may take a little while, so you can start reading the rest of this page while you wait.


## Part 2 - using the data for Web query classification

### Tranforming the data into features

Let's now convert our raw texts into sets of features. We will do this using a vocabulary of character ngrams. The repository contains scripts to compute ngram frequencies for each category. You can run it doing:

    python3 ngrams.py [ngram-size]

For instance,

    python3 ngrams.py 6

will create a file in each subfolder of *data/categories*, showing a sorted list of ngrams of size 6.

We probably want several ngram sizes. So re-run the script for size 4-6, for instance.


### Feature selection

Which of our features should we use to generate document representations? A common way to do this in Information Retrieval is the TF-IDF measure.

Check out the definition of TF-IDF here: [https://en.wikipedia.org/wiki/Tf%E2%80%93idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). Can you explain how to use that measure in our setting, where each person is responsible for one Wikipedia category?

Next, we will want to compute the td-idf of each ngram in each category. You can do this by running:

    python3 output_top_tfidf_ngrams.py

This will create a *tf_idfs.txt* file in each category subfolder. In addition, the script captures the 100 ngrams with highest tf-idf *for each category* and uses them to generate a set of features, saved in the file *data/vocab.txt*. In essence, what we are doing here is simple feature selection, based on the highest-ranked ngrams across categories.

Now that we have our features, we can build vector representations for each category. If we have ended up with 1000 features in our feature selection step, we will build 1000-dimensional vectors to represent each category, with each component of a vector set to the tf-idf of the relevant dimensions for that category. As an example, if *actor* is the 16th dimension in our 1000-dimensional space, and category *russian_language_films* has a tf-idf of 1.147e-05 for that ngram, then dimension 16 will be set to that number in the *russian_language_film* vector.

You can create your category vectors with

    python3 mk_cat_vectors.py

## Mapping queries to topics

Our final goal for now is to see how we can map incoming search queries to each category. The point of this is that, as our search engine grows (to potentially millions, or billions of pages), it would be very inefficient to try and find the answer to a movie-related query in our "gecko and other lizards" category. We want to narrow things down.

So let's test this. The file *query_file.txt* contains some sample queries. You should change this file and write down queries corresponding to the categories you selected, one query per line. We want to see whether the system finds the right category for each query. Run the following:

    python3 classify.py query_file.txt

and you will return a ranked list of categories for each query. You of course want to most relevant categories at the top.

Play with the *classify.py* script, and with adding queries to the file. What works, what doesn't? Why?

 
