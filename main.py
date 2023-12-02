import glob
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from argparse import ArgumentParser

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

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

    print("\n--- Web Crawling ---\n")

    # Create and run a CrawlerProcess based on the spider
    process = CrawlerProcess()
    process.crawl(MainSpider, max_files=args.num_files)
    process.start()

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_df=0.1, min_df=5, stop_words='english', strip_accents='unicode', input='filename',
                                 encoding="utf-8")

    print("\n--- Vectorization ---")

    # Vectorize the text files
    X_tfidf = vectorizer.fit_transform(glob.glob('text_files/*'))

    print(f"\nn_samples: {X_tfidf.shape[0]}, n_features: {X_tfidf.shape[1]}")

    print(f"\n{X_tfidf.nnz / np.prod(X_tfidf.shape):.3f}")

    print("\n--- LSA Dimensionality Reduction ---")

    # Perform LSA dimensionality reduction
    lsa = make_pipeline(TruncatedSVD(n_components=100), Normalizer(copy=False))
    X_lsa = lsa.fit_transform(X_tfidf)
    explained_variance = lsa[0].explained_variance_ratio_.sum()

    print(f"\nExplained variance of the SVD step: {explained_variance * 100:.1f}%")

    print("\n--- K-Means (k=3) ---")

    # Perform K-Means where k=3
    kmeans_3 = KMeans(max_iter=100, n_clusters=3, random_state=3, n_init=1).fit(X_lsa)

    cluster_ids, cluster_sizes = np.unique(kmeans_3.labels_, return_counts=True)

    print(f"\nNumber of elements assigned to each cluster (KMEANS 3): {cluster_sizes}")

    # Compute top terms per cluster, when k=3
    print("\nTop terms per cluster, when k=3:\n")
    original_space_centroids = lsa[0].inverse_transform(kmeans_3.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(3):
        print(f"Cluster {i}: ", end="")
        for ind in order_centroids[i, :10]:
            print(f"{terms[ind]} ", end="")
        print()

    print("\n--- K-Means (k=6) ---")

    # Perform K-Means where k=3
    kmeans_6 = KMeans(max_iter=100, n_clusters=6, random_state=6, n_init=1).fit(X_lsa)

    cluster_ids, cluster_sizes = np.unique(kmeans_6.labels_, return_counts=True)

    print(f"\nNumber of elements assigned to each cluster (KMEANS 6): {cluster_sizes}")

    # Compute top terms per cluster, when k=3
    print("\nTop terms per cluster, when k=6:\n")
    original_space_centroids = lsa[0].inverse_transform(kmeans_6.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(6):
        print(f"Cluster {i}: ", end="")
        for ind in order_centroids[i, :10]:
            print(f"{terms[ind]} ", end="")
        print()


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
