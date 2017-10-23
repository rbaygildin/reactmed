import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sklearn.decomposition as decomp
from apps.analytics.visualizers.base_visualizer import *


#Changed
class PCAVisualizer(Visualizer):
    def visualize(self, df, **kwargs):
        res = {}
        df = df.copy()

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        # Alpha
        alpha = kwargs.get('alpha', self.alpha)

        # Figure size
        # figsize = kwargs.get('figsize', self.figsize)
        figsize = (12, 6)
        print(figsize)

        # Class column
        class_col = kwargs.get('class_col', self.class_col)

        classes = df[class_col].drop_duplicates().values

        # Color map
        color_map = kwargs.get('color_map', self.color_map)
        cmap = class_color(classes, color_map=color_map)

        # Patients
        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {df.index.get_loc(p['patient_id']): p for p in patients.to_dict('records')}
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)
        pca = decomp.PCA(n_components=2)
        kls_ser = df[class_col]
        del df[class_col]
        pca.fit(df)
        df = pca.transform(df)
        for kls in classes:
            kls_df = df[kls_ser == kls]
            i2p_id = {kls_df.index.get_loc(p_id): p_id for p_id in kls_df.index.values}
            del kls_df[class_col]
            pca = decomp.PCA(n_components=2)
            pca.fit(kls_df)
            kls_df = pca.transform(kls_df)
            m = df.shape[0]
            points, = plt.plot(kls_df[:, 0], kls_df[:, 1], 'o', label=kls, alpha=alpha, c=cmap(kls))
            kls_color = points.get_color()
            for i in range(m):
                if patients is not None:
                    p_id = i2p_id[i]
                    patient = patients.get(p_id, None)
                    if patient is not None:
                        plt.plot(kls_df[i, 0], kls_df[i, 1], '8', c=kls_color, zorder=5, markersize=16,
                                 markeredgecolor='black', markeredgewidth=2)
                        plt.plot(kls_df[i, 0], kls_df[i, 1], 'x', c='black', zorder=6, markersize=8, markeredgewidth=1)
                        ax.annotate(patient['full_name'], xy=(kls_df[i, 0], kls_df[i, 1]), xycoords='data',
                                    xytext=(-40, 40), textcoords='offset points', ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                                    arrowprops=dict(facecolor='black'),
                                    zorder=7
                                    )
        exp_var = pca.explained_variance_ratio_
        plt.xlabel('PCA 1: %.2f%%' % (exp_var[0] * 100))
        plt.ylabel('PCA 2: %.2f%%' % (exp_var[1] * 100))
        plt.legend(title=class_col, handles=[mpatches.Patch(color=cmap(kls), label=kls) for kls in classes],
                   shadow=True, fancybox=True, loc=1)
        # plt.legend(shadow=True, fancybox=True, loc=1, title=class_col)
        fig.savefig(out, format=img_format)