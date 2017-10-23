from abc import ABCMeta

import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import sklearn.decomposition as decomp
import time
from scipy.spatial.distance import pdist, cdist
from sklearn.metrics import silhouette_score

from apps.analytics.visualizers.base_visualizer import *


class CentroidsClusteringVisualizer(Visualizer, metaclass=ABCMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Number of clusters
        self.n_clusters = kwargs.get('n_clusters', 2)
        self.n_clusters_min = 1
        self.n_clusters_max = 15
        if isinstance(self.n_clusters, list):
            if len(self.n_clusters) == 1:
                self.n_clusters_min = int(self.n_clusters[0])
                self.n_clusters_max = int(self.n_clusters[0])
            elif len(self.n_clusters) == 2:
                self.n_clusters_min = int(self.n_clusters[0])
                self.n_clusters_max = int(self.n_clusters[1])
        elif isinstance(self.n_clusters, int):
            self.n_clusters_min = self.n_clusters
            self.n_clusters_max = self.n_clusters
        # Performance method
        self.perf_method = kwargs.get('perf_method', 'none')
        # Width
        self.width = kwargs.get('width', 8)
        # Height
        self.height = kwargs.get('height', 8)
        # Number of clustering plots
        self.n_cluster_plots = self.n_clusters_max - self.n_clusters_min + 1
        if self.perf_method == 'elbow':
            self.plt_count = self.n_cluster_plots + 2
        elif self.perf_method == 'silhouette':
            self.plt_count = self.n_cluster_plots + 1
        else:
            self.plt_count = self.n_cluster_plots
        # Figure size
        self.figsize = kwargs.get('figsize', (self.width, self.height * self.plt_count))

    @staticmethod
    def elbow_method(x, cm_vars):
        centroids = [cm_var.cluster_centers_ for cm_var in cm_vars.values()]
        cluster_dist = [cdist(x, centroid, 'euclidean') for centroid in centroids]
        dist = [np.min(cd, axis=1) for cd in cluster_dist]
        ss = [sum(d ** 2) for d in dist]
        tss = sum(pdist(x) ** 2) / x.shape[0]
        ess = tss - ss
        return tss, ess, ss, (ess / tss) * 100

    @staticmethod
    def silhouette_method(x, cm_vars):
        sm_vars = {}
        for cm_key in cm_vars.keys():
            sm_vars[cm_key] = silhouette_score(x, cm_vars[cm_key].labels_)
        return sm_vars

    @abstractmethod
    def cluster(self, df, **kwargs):
        pass

    def visualize(self, df, **kwargs):

        df = df.copy()

        if isinstance(self.patients, pd.DataFrame):
            self.patients = {df.index.get_loc(p['patient_id']): p for p in self.patients.to_dict('records')}
        if isinstance(df, pd.DataFrame):
            df = df.as_matrix()
        n = df.shape[1]
        cluster_labels = {}
        df = standardize(df)
        cm_vars = self.cluster(df)
        if n > 2:
            pca = decomp.PCA(n_components=2)
            pca.fit(df)
            df2 = pca.transform(df)
        else:
            df2 = df
        fig = plt.figure(figsize=self.figsize)
        for n_cluster_i in range(self.n_clusters_min, self.n_clusters_max + 1):
            plt_i = n_cluster_i - self.n_clusters_min + 1
            cm = cm_vars[n_cluster_i]
            if n > 2:
                cluster_centers = pca.transform(cm.cluster_centers_)
            else:
                cluster_centers = cm.cluster_centers_
            ax = fig.add_subplot(self.plt_count, 1, plt_i)
            self.n_clusters = len(np.unique(cm.labels_))
            cmap = class_color(list(range(self.n_clusters)), color_map=self.color_map)
            t1 = time.time()
            for i in range(self.n_clusters):
                cluster_labels[i] = plt.scatter(df2[cm.labels_ == i, 0], df2[cm.labels_ == i, 1],
                                                c=cmap(i),
                                                marker='o',
                                                linewidths=3, alpha=self.alpha
                                                )
            if self.patients is not None:
                for i, patient in self.patients.items():
                    ax.annotate(patient['full_name'], xy=(df2[i, 0], df2[i, 1]), xycoords='data',
                                xytext=(-20, 20),
                                textcoords='offset points', ha='right', va='bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                                )
            plt.plot(cluster_centers[:, 0], cluster_centers[:, 1], "x", zorder=10, c='black',
                     markersize=12, markeredgewidth=3)
            plt.legend(cluster_labels.values(), ['Cluster %d' % cl_i for cl_i in range(len(cluster_labels))])
            plt.title('K Means - Clusters %d' % n_cluster_i)
            t2 = time.time()
            print("K Means Draw Total Time: %f" % ((t2 - t1) * 1000))
        if self.perf_method == 'elbow':
            em_res = CentroidsClusteringVisualizer.elbow_method(df, cm_vars)
            ess_p = em_res[3]
            ss = em_res[2]
            # Within cluster variance
            ax = fig.add_subplot(self.plt_count, 1, self.n_cluster_plots + 1)
            plt.title('Elbow method for K Means Clustering')
            plt.plot(list(range(self.n_clusters_min, self.n_clusters_max + 1)), ss)
            plt.scatter(list(range(self.n_clusters_min, self.n_clusters_max + 1)), ss)
            plt.xlabel('Number of clusters')
            plt.ylabel('Within cluster variance')
            ax.set_xticks(list(range(self.n_clusters_min, self.n_clusters_max + 1)))
            plt.grid()
            # Explained variance
            ax = fig.add_subplot(self.plt_count, 1, self.n_cluster_plots + 2)
            plt.title('Elbow method for K Means Clustering')
            plt.plot(list(range(self.n_clusters_min, self.n_clusters_max + 1)), ess_p)
            plt.scatter(list(range(self.n_clusters_min, self.n_clusters_max + 1)), ess_p)
            plt.xlabel('Number of clusters')
            plt.ylabel('Explained variance percentage (%)')
            ax.set_xticks(list(range(self.n_clusters_min, self.n_clusters_max + 1)))
            plt.grid()
        if self.perf_method == 'silhouette':
            silhouette_avg = list(CentroidsClusteringVisualizer.silhouette_method(df, cm_vars).values())
            # Within cluster variance
            ax = fig.add_subplot(self.plt_count, 1, self.n_cluster_plots + 1)
            plt.title('Silhouette Method for K Means Clustering')
            plt.plot(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
            plt.scatter(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
            plt.xlabel('Number of clusters')
            plt.ylabel('Silhouette score')
            ax.set_xticks(list(range(self.n_clusters_min, self.n_clusters_max + 1)))
            plt.grid()
        plt.tight_layout()
        t1 = time.time() * 1000
        fig.savefig(self.out, format=self.img_format)
        t2 = time.time() * 1000
        print("Save figure: %f" % (t2 - t1))
