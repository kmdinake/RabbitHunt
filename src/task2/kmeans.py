import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class KMeansAgent:
    n_clusters = None

    def __init__(self):
        self.n_clusters = 3  # default number of clusters for KMeans

    def set_n_clusters(self, n_clusters):
        if isinstance(n_clusters, int):
            self.n_clusters = n_clusters
        else:
            print("Number of clusters must be an integer!")
            return

    @staticmethod
    def get_optimum_cluster(arr):
        if None is arr or len(arr) == 0:
            print("Cannot determine optimum clusters on an empty list!")
            return None, None
        # calc absolute dist of each cluster's silhouette score
        # to it's adjacent cluster's silhouette score
        dist = list()
        for i in range(len(arr) - 1):
            dist.append(np.abs(arr[i]['silhouette_score'] - arr[i + 1]['silhouette_score']))
        # get the one with the steepest difference in the silhouette score
        highest_index = 0
        highest = dist[highest_index]
        for i in range(1, len(dist)):
            if dist[i] > highest:
                highest_index = i
                highest = dist[highest_index]
        cluster_centers = arr[highest_index + 1]['cluster_centers']
        cluster_labels = arr[highest_index + 1]['cluster_labels']
        # n_clusters = arr[highest_index + 1]['n_clusters']
        return cluster_centers, cluster_labels

    def train(self, dataset):
        possible_clusters = list()
        range_n_clusters = range(2, 11)
        for n_clusters in range_n_clusters:
            self.set_n_clusters(n_clusters=n_clusters)
            model = KMeans(n_clusters=self.n_clusters)
            model_labels = model.fit_predict(dataset)
            temp_cluster = {'n_clusters': self.n_clusters, 'cluster_centers': model.cluster_centers_,
                            'cluster_labels': model.labels_,
                            'silhouette_score': silhouette_score(dataset, model_labels)}
            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density
            # and separation of the formed clusters
            possible_clusters.append(temp_cluster)
        return self.get_optimum_cluster(possible_clusters)