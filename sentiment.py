import glob

from afinn import Afinn


def main():
    print('\n--- AFINN Sentiment Analysis ---\n')

    # Get all clusters from the files
    clusters = _get_clusters()

    print('\n\t~~~ Manual AFINN ~~~\n')

    manual_AFINN(clusters)

    print('\n\t~~~ Library AFINN ~~~\n')

    library_AFINN(clusters)


def library_AFINN(clusters):
    """
    Given a list of clusters, score them automatically by using the `afinn` library
    :param clusters: The list of clusters to score
    """

    afinn_lib = Afinn()

    for i, cluster in enumerate(clusters):
        cluster = ' '.join(word for word in cluster)

        print(f"\tCluster {i}: {cluster}, Score: {afinn_lib.score(cluster)}\n")


def manual_AFINN(clusters):
    """
    Given a list of clusters, score the manually using a custom algorithm

    :param clusters: The list of clusters to score
    """

    for i, cluster in enumerate(clusters):
        print(f"\tCluster {i}: {cluster}, Score: {_score_cluster_manual(cluster)}\n")


def _score_cluster_manual(cluster: list) -> float:
    """
    Score a given cluster manually, using a custom algorithm

    :param cluster: The cluster to give a sentiment score to. Negative numbers are negative and vice-versa
    :return: The score for the cluster
    """

    # Get the AFINN dict from AFINN-111.txt
    AFINN = get_AFINN()

    # The score for a cluster starts at 0, neutral sentiment
    cluster_score = 0

    for word in cluster:
        # Try to find the word in the lexicon. If not found, score is 0
        word_score = int(AFINN.get(word, 0))

        # Modify the overall cluster score by the score for this word
        cluster_score += word_score

    return cluster_score


def _get_clusters():
    """
    Get all clusters from the files

    :return: The clusters
    """

    clusters = []

    files = glob.glob('clusters/k6/*')

    for file in files:
        with open(file, 'rt') as f:
            cluster = f.read().split(' ')

            clusters.append(cluster)

    return clusters


def get_AFINN() -> dict:
    """
    Read the AFINN-111 lexicon and return the dict form of it

    :return: The dict from of the AFINN-111 lexicon
    """

    afinn = {}

    with open('AFINN-111.txt', 'rt') as f:
        contents = f.readlines()

    for line in contents:
        line = line.strip().replace('\t', ' ').split(' ')
        afinn[line[0]] = line[1]

    return afinn


if __name__ == '__main__':
    main()
