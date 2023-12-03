import glob


def main():
    # Get all clusters from the files
    clusters = _get_clusters()

    AFINN = get_AFINN()

    for i, cluster in enumerate(clusters):
        print(f'\n--- CLUSTER {i} ---\n')

        print(f"Cluster: {cluster}, Score: {_score_cluster(cluster, AFINN)}")


def _score_cluster(cluster: list, AFINN: dict) -> float:
    len_cluster = len(cluster)

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
