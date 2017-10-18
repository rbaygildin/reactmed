import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.cluster as cluster
import sklearn.decomposition as decomp
import time
from sklearn.metrics import silhouette_score

from apps.analytics.visualizers.base_visualizer import *


class AgglomerativeClusteringVisualizer(Visualizer):
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
        self.linkage = kwargs.get('linkage', 'average')
        self.n_neighbors = kwargs.get('n_neighbors', 2)

    @staticmethod
    def silhouette_method(x, cm_vars):
        sm_vars = {}
        for cm_key in cm_vars.keys():
            sm_vars[cm_key] = silhouette_score(x, cm_vars[cm_key].labels_)
        return sm_vars

    def cluster(self, df, **kwargs):
        cm_vars = {}
        for n_cluster_i in range(self.n_clusters_min, self.n_clusters_max + 1):
            t1 = time.time() * 1000
            cm_vars[n_cluster_i] = cluster.AgglomerativeClustering(n_clusters=n_cluster_i, linkage=self.linkage)
            cm_vars[n_cluster_i].fit(df)
            t2 = time.time() * 1000
            print("Agglomerative fitted (clusters = %d): %f" % (n_cluster_i, t2 - t1))
        return cm_vars

    def visualize(self, df, **kwargs):

        df = df.copy()

        # Patients
        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {df.index.get_loc(p['patient_id']): p for p in patients.to_dict('records')}
        if isinstance(df, pd.DataFrame):
            df = df.as_matrix()
        cluster_labels = {}
        df = standardize(df)
        cm_vars = self.cluster(df)
        n = df.shape[1]
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
            ax = fig.add_subplot(self.plt_count, 1, plt_i)
            n_clusters = len(np.unique(cm.labels_))
            cmap = class_color(list(range(n_clusters)), color_map=self.color_map)
            for i in range(n_clusters):
                cluster_labels[i] = plt.scatter(df2[cm.labels_ == i, 0], df2[cm.labels_ == i, 1],
                                                c=cmap(i),
                                                marker='o',
                                                linewidths=3, alpha=self.alpha
                                                )
            if patients is not None:
                for i, patient in patients.items():
                    ax.annotate(patient['full_name'], xy=(df2[i, 0], df2[i, 1]), xycoords='data',
                                xytext=(-20, 20),
                                textcoords='offset points', ha='right', va='bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                                )
            plt.legend(cluster_labels.values(), ['Cluster %d' % cl_i for cl_i in range(len(cluster_labels))])
            plt.title('Agglomerative Clustering - Clusters %d' % n_cluster_i)
        if self.perf_method == 'silhouette':
            silhouette_avg = list(AgglomerativeClusteringVisualizer.silhouette_method(df, cm_vars).values())
            ax = fig.add_subplot(self.plt_count, 1, self.n_cluster_plots + 1)
            plt.title('Silhouette Method for Agglomerative Clustering')
            plt.plot(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
            plt.scatter(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
            plt.xlabel('Number of clusters')
            plt.ylabel('Silhouette score')
            ax.set_xticks(list(range(self.n_clusters_min, self.n_clusters_max + 1)))
            plt.grid()
        plt.tight_layout()
        fig.savefig(self.out, format=self.img_format)
