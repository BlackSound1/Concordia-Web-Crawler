# COMP479P4

<hr />

The `AFINN-111.txt` lexicon was sourced from: http://corpustext.com/reference/sentiment_afinn.html.

The strategy for clustering was sourced from: https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html.

The Afinn 0.1 library was sourced from: https://github.com/fnielsen/afinn.

The Scrapy 2.8.0 library was sourced from: https://github.com/scrapy/scrapy. Basic scrapy usage was inspired by:
https://docs.scrapy.org/en/latest/intro/tutorial.html.
Using Scrapy within Python was inspired by: https://stackoverflow.com/a/31374345.

The Scikit-learn 1.3.0 library was sourced from: https://anaconda.org/conda-forge/scikit-learn.

## Setup

1. Navigate to this directory.

2. Create a virtual environment with:

    ```shell
    $ python -m venv COMP479
    ```

3. Activate it with:

    ```shell
    $ source COMP479\Scripts\activate.bat
    ```

4. Install the dependencies with:

    ```shell
    $ pip install -r requirements.txt
    ```

## To Run

First run the `crawl.py` module with:

```shell
$ python crawl.py -n 1000
```

The `-n` flag determines how many documents to crawl and download. Due to some potential errors found when performing 
clustering on a small numer of files, please set `-n` to a large number.

Then, run the `cluster.py` module with:

```shell
$ python cluster.py
```

Finally, run the `sentiment.py` module with:

```shell
$ python sentiment.py
```

## Sequences of Calls

### Crawling

In `crawl.py`, use the external library Scrapy https://github.com/scrapy/scrapy. 
I create a `CrawlerProcess` object that lets me use Scrapy from within Python, not the command line.
I pass the parameter `max_files` to it, which is set to the `-n` argument passed in via the `$ python crawl.py -n 1000`
call above. If none is provided, `max_files` is set to 100 by default.

The `MainSpiders` parameters include:

- `name = 'test'`: The name of the spider.
- `allowed_domains = ['www.concordia.ca']`: should hopefully keep the
crawler on Concordia websites.
- `start_urls = ['https://www.concordia.ca']`: Makes the crawler start on the Concordia Homepage.
- `num_files = 0`: Keeps track of how many files have been downloaded.

In the `update_settings()` method of the spider, I set it to obey `robots.txt` using the line:

```python
settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')
```

### Parsing

The BeautifulSoup library is used to parse the cralwed web text. It uses the following parameters:

- `features="html.parser"`: makes the BeautifulSoup parser treat each document as HTML.
- `from_encoding='utf-8'`: Forces the documents to
be interpreted using UTF-8 encoding. Some encoding errors were noticed when this wasn't set. 

### Vectorizing

In `cluster.py`, the `TfidfVectorizer` vectorizer is used to vectorize the documents.
It's paramters include:

- `max_df=0.5`: sets the vectorizer to ignore terms that occur in more that 50% of the documents.
- `min_df=0.1`: makes it ignore all terms that occur in fewer than 10% of all documents.
- `stop_words=stopwords`: lets me set a custom set 
of stopwords to ignore when vectorizing. I made a custom set composed of all English and French stopwords, plus several
others found in experiment.
- `strip_accents='unicode'`: Strips all accents according to Unicode (not ASCII) standards
- `input='filename'`: Sets the input for the `fit_transform()` method take a list of filenames.
- `encoding="utf-8"`: Forces UTF-8 encoding.

### K-Means

In `cluster.py`, the `KMeans` classifier is used from `sklearn`. It's parameters include:

- `max_iter=100`: Sets the maximum number of iterations for a single K-Means run to 100.
- `n_clusters`: Sets the number of clusters (and centroids) to create. For the `k=3` run, this number is 3,
                likewise for when `k=6`.
- `random_state`: Sets a seed for randomness to hopefully generate reproducible results. Set to 3 when `k=3`, likewise
                  for when `k=6`.
- `n_init=1`: Set the number of times the K-Means algorithm is run with different centroid seeds to 1.

### Sentiment Analysis

In `sentiment.py`, sentiment analysis is done on the discovered clusters two times. The first time is via the
algorithm I came up with. The second is via the algorithm found in the Python `afinn` library.
As it turns out, these are the same algorithm, but I worked on my algorithm before even downloading the `afinn` library,
so I wouldn't have known that. After I did know they were the same algorithm, I decided to keep mine the way it is
because I knew I had something to say about their differing performance for some clusters.

For my algorithm, I use the `AFINN-111.txt` lexicon. For each cluster, I score each word according to this lexicon and
add up each word's score into a final cluster score.

For the library algorithm, for each cluster, I feed the entire cluster as one string to `afinn.score()`.
The library algorithm uses the `AFINN-en-165.txt` lexicon by default. Since these are different lexicons, this easily
explains any minor differing scores.
