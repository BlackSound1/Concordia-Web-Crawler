import glob
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from argparse import ArgumentParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

from P4.spiders.MainSpider import MainSpider


# Create an argument parser to let user decide how many files to process
parser = ArgumentParser(description="Concordia Scraper")
parser.add_argument('--num-files', '-n', metavar='n', type=int,
                    help="The number of files to process", default=10, required=False)


def main():

    # Parse the command-line arguments passed to this script, if any
    args = parser.parse_args()

    # Clear the file folder(s)
    clear_folder()

    # Create and run a CrawlerProcess based on the spider
    process = CrawlerProcess()
    process.crawl(MainSpider, max_files=args.num_files)
    process.start()

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_df=0.1, min_df=5, stop_words='english', strip_accents='unicode', input='filename',
                                 encoding="utf-8")

    # Vectorize the text files
    X_tfidf = vectorizer.fit_transform(glob.glob('text_files/*'))

    print(f"\nn_samples: {X_tfidf.shape[0]}, n_features: {X_tfidf.shape[1]}")

    print(f"\n{X_tfidf.nnz / np.prod(X_tfidf.shape):.3f}")


def clear_folder():
    """
    Delete the contents of html_files when starting the app.
    """

    # for path in Path('html_files/').glob('*'):
    #     if path.is_file():
    #         path.unlink()

    for path in Path('text_files/').glob('*'):
        if path.is_file():
            path.unlink()


if __name__ == '__main__':
    main()
