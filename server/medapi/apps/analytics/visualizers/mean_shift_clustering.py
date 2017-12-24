from apps.analytics.visualizers.base_visualizer import *

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.cluster as cluster
import sklearn.decomposition as decomp
import time


class MeanShiftClusteringVisualizer(Visualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Width
        self.width = kwargs.get('width', 8)
        # Height
        self.height = kwargs.get('height', 8)
        self.perf_method = kwargs.get('perf_method', 'none')
        self.plt_count = 1
        if self.perf_method == 'silhouette':
            self.figsize = kwargs.get('figsize', (self.width, self.height * 2))
            self.plt_count = 2
        else:
            self.figsize = kwargs.get('figsize', (self.width, self.height))
        self.n_clusters = kwargs.get('n_clusters', 2)
        self.linkage = kwargs.get('linkage', 'average')
        self.n_neighbors = kwargs.get('n_neighbors', 2)
        self.bandwidth = kwargs.get('bandwidth', None)
        self.quantile = kwargs.get('quantile', 0.3)
        self.n_samples = kwargs.get('n_samples', None)

    def visualize(self, df, **kwargs):

        df = df.copy()

        # Patients
        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {df.index.get_loc(p['patient_id']): p for p in patients.to_dict('records')}
        if isinstance(df, pd.DataFrame):
            df = df.as_matrix()

        figsize = kwargs.get('figsize', self.figsize)
        cluster_labels = {}
        df = standardize(df)
        n = df.shape[1]
        if n > 2:
            pca = decomp.PCA(n_components=2)
            pca.fit(df)
            df2 = pca.transform(df)
        else:
            df2 = df
        fig = plt.figure(figsize=figsize)
        if self.bandwidth is None:
            self.bandwidth = cluster.estimate_bandwidth(df, quantile=self.quantile)
        t1 = time.time() * 1000
        mean_shift = cluster.MeanShift(bandwidth=self.bandwidth, bin_seeding=True)
        mean_shift.fit(df)
        t2 = time.time() * 1000
        print("Mean Shift Time Total: %f" % (t2 - t1))
        ax = fig.add_subplot(1, 1, 1)
        n_clusters = len(np.unique(mean_shift.labels_))
        cmap = class_color(list(range(n_clusters)), color_map=self.color_map)
        t1 = time.time()
        for i in range(n_clusters):
            cluster_labels[i] = plt.scatter(df2[mean_shift.labels_ == i, 0], df2[mean_shift.labels_ == i, 1],
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
        plt.plot(mean_shift.cluster_centers_[:, 0], mean_shift.cluster_centers_[:, 1], "x", zorder=10, c='black',
                 markersize=12, markeredgewidth=3)
        plt.legend(cluster_labels.values(), ['Cluster %d' % cl_i for cl_i in range(len(cluster_labels))])
        plt.title('Mean Shift Clustering: Estimated clusters %d' % n_clusters)
        # if self.perf_method == 'silhouette':
        #     silhouette_avg = list(AgglomerativeClusteringVisualizer.silhouette_method(df, cm_vars).values())
        #     ax = fig.add_subplot(self.plt_count, 1, self.plt_count)
        #     plt.title('Silhouette Method for Agglomerative Clustering')
        #     plt.plot(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
        #     plt.scatter(list(range(self.n_clusters_min, self.n_clusters_max + 1)), silhouette_avg)
        #     plt.xlabel('Number of clusters')
        #     plt.ylabel('Silhouette score')
        #     ax.set_xticks(list(range(self.n_clusters_min, self.n_clusters_max + 1)))
        #     plt.grid()
        plt.tight_layout()
        t2 = time.time()
        print("Mean Shift Draw Total Time: %f" % ((t2 - t1) * 1000))
        fig.savefig(self.out, format=self.img_format)
