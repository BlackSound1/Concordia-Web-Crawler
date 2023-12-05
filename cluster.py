import glob
import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from nltk.corpus import stopwords

# Create an argument parser to let user decide how many downloaded files to process
parser = ArgumentParser(description="Concordia Clusterer")
parser.add_argument('--num-files', '-n', type=int,
                    help="The number of files to process", required=False)

# Create a custom stopwords list composed of all English and French stopwords, plus a list of other
# stopwords found in experiment
stopwords = (
        stopwords.words('english') +
        stopwords.words('french') +
        ['etaient', 'etais', 'etait', 'etant', 'etante', 'etantes',
         'etants', 'ete', 'etee', 'etees', 'etes', 'etiez', 'etions',
         'eumes', 'eutes', 'fumes', 'futes', 'meme', 'co', 'ca', 'cu', 'el']
)


def main():
    """
    Note that this module is heavily inspired by
    https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html

    Using Sklearn 1.3.0 https://github.com/scikit-learn/scikit-learn
    """

    # Parse the command-line arguments passed to this script, if any
    args = parser.parse_args()

    print("\n--- Vectorization ---")

    # Create a TF-IDF vectorizer
    try:
        vectorizer = TfidfVectorizer(max_df=0.5, min_df=0.1, stop_words=stopwords, strip_accents='unicode',
                                     input='filename', encoding="utf-8")
    except ValueError as e:
        tb = sys.exc_info()[2]
        print(f"\nVECTORIZATION ERROR: {e.with_traceback(tb)} \n")
        return

    # Get the number of files to process
    ALL_FILES = glob.glob('text_files/*')
    if args.num_files is None or args.num_files > len(ALL_FILES):
        print(
            f"\nYou entered {args.num_files} files, but only {len(ALL_FILES)} are present. Will process all of them\n")
        num_files = len(ALL_FILES)
    else:
        num_files = args.num_files

    # Vectorize the text files
    X_tfidf = vectorizer.fit_transform(ALL_FILES[:num_files])

    n_samples = X_tfidf.shape[0]
    n_features = X_tfidf.shape[1]
    print(f"\nn_samples: {n_samples}, n_features: {n_features}")

    print(f"\n{X_tfidf.nnz / np.prod(X_tfidf.shape):.3f}")

    print("\n--- LSA Dimensionality Reduction ---")

    # Perform LSA dimensionality reduction
    try:
        lsa = make_pipeline(TruncatedSVD(n_components=n_features if n_features < 100 else 100),
                            Normalizer(copy=False))
    except ValueError as e:
        tb = sys.exc_info()[2]
        print(f"\nLSA PIPELINE ERROR: {e.with_traceback(tb)} \n")
        return

    try:
        X_lsa = lsa.fit_transform(X_tfidf)
    except ValueError as e:
        tb = sys.exc_info()[2]
        print(f"\nLSA FIT TRANSFORM ERROR:  {e.with_traceback(tb)} \n")
        return

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

    # Print most representative terms for each cluster
    _save_clusters(order_centroids, terms, folder='clusters/k3/', k=3)

    print("\n--- K-Means (k=6) ---")

    # Perform K-Means where k=3
    kmeans_6 = KMeans(max_iter=100, n_clusters=6, random_state=6, n_init=1).fit(X_lsa)

    cluster_ids, cluster_sizes = np.unique(kmeans_6.labels_, return_counts=True)

    print(f"\nNumber of elements assigned to each cluster (KMEANS 6): {cluster_sizes}")

    # Compute top terms per cluster, when k=6
    print("\nTop terms per cluster, when k=6:\n")
    original_space_centroids = lsa[0].inverse_transform(kmeans_6.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    # Print most representative terms for each cluster
    _save_clusters(order_centroids, terms, folder='clusters/k6/', k=6)


def _save_clusters(order_centroids: list, terms: list, folder: str, k: int) -> None:
    """
    Display and save the resulting clusters from K-Means clustering

    :param order_centroids: The order centroids to base the clusters on
    :param terms: The terms to base the clusters on
    :param folder: The folder to save to
    :param k: Whether k=3 or k=6
    """

    Path(folder).mkdir(parents=True, exist_ok=True)  # Make sure path to cluster files exists

    # Loop through each cluster
    for i in range(k):
        cluster = []
        # print(f"Cluster {i} sample: ", end="")
        print(f"Cluster {i}: ", end="")
        for ind in order_centroids[i, :20]:
            cluster.append(terms[ind])
            print(f"{terms[ind]} ", end="")
        # print("...")
        print()

        with open(f"{folder}cluster-{i}.txt", 'wt') as f:
            f.write(' '.join(j for j in cluster))

        # cluster = []  # Create an empty list for this full cluster
        #
        # # Add to the empty list each element in the full cluster
        # for ind in order_centroids[i]:
        #     cluster.append(terms[ind])
        #
        # # Save entire cluster to file for sentiment analysis later
        # with open(f"{folder}cluster-{i}.txt", 'wt') as f:
        #     f.write(' '.join(j for j in cluster))


if __name__ == '__main__':
    main()
