import matplotlib

matplotlib.use('Agg')

import sklearn.cluster as cluster

from apps.analytics.visualizers.base_centroids_clustering import *


class KMeansClusteringVisualizer(CentroidsClusteringVisualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_jobs = 4
        self.algorithm = 'elkan'

    def cluster(self, df, **kwargs):
        cm_vars = {}
        for n_cluster_i in range(self.n_clusters_min, self.n_clusters_max + 1):
            t1 = time.time() * 1000
            cm_vars[n_cluster_i] = cluster.KMeans(n_clusters=n_cluster_i, algorithm=self.algorithm)
            cm_vars[n_cluster_i].fit(df)
            t2 = time.time() * 1000
            print("K Means fitted (clusters = %d): %f" % (n_cluster_i, t2 - t1))
        return cm_vars
