from apps.analytics.visualizers.base_visualizer import *

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class ParallelCoordinatesVisualizer(Visualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def visualize(self, df, **kwargs):
        df = df.copy()
        m = len(df)

        # Class column
        class_col = kwargs.get('class_col', self.class_col)
        kls_df = df[class_col]
        classes = df[class_col].drop_duplicates().values
        del df[class_col]

        n_cols = len(df.columns)

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        # Figure size
        figsize = kwargs.get('figsize', (3 * n_cols, 8))

        # Alpha
        alpha = kwargs.get('alpha', self.alpha)

        # Color map
        color_map = kwargs.get('color_map', self.color_map)

        # Feature columns
        feature_cols = kwargs.get('feature_cols', self.feature_cols)

        # If feature columns were chosen we delete others from data frame
        if feature_cols is not None:
            df = df[[col for col in feature_cols]]

        x = range(1, n_cols + 1)

        # Patients
        patients = kwargs.get('patients', self.patients)

        cmap = class_color(classes, color_map=color_map)
        if isinstance(patients, pd.DataFrame):
            patients = {df.index.get_loc(p['patient_id']): p for p in patients.to_dict('records')}
        if patients is not None:
            p2cmap = class_color(list(patients.keys()), color_map=color_map, invert=True)
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        for i in x:
            ax.axvline(i, color='black', linewidth=1)
        plh = {}
        for i in range(m):
            kls = kls_df.iat[i]
            y = df.iloc[i]
            plt.plot(x, y, marker='o', c=cmap(kls), alpha=alpha, antialiased=True)
            patient_id = df.index.values[i]
            if patients is not None:
                patient = patients.get(patient_id, None)
                if patient is not None:
                    plh[patient_id] = []
                    # dashed line
                    d_line, = plt.plot(x, y, c=cmap(kls), alpha=1.0, linewidth=5, linestyle='--', zorder=5)
                    # circle
                    #                 plt.plot(points, ac_series_points, c=p2cmap(patient_id), marker='o', zorder=5, linewidth=7)
                    c_marker, = plt.plot(x, y, 'o', c=p2cmap(patient_id), zorder=6, markersize=16)
                    # cross
                    #                 plt.scatter(points, ac_series_points, c="white", marker='x', zorder=6, linewidth=2)
                    crs_marker, = plt.plot(x, y, 'x', c='white', zorder=6, markersize=10, markeredgewidth=2)
                    plt.fill_between(x, y - np.full(shape=len(y), fill_value=0.4),
                                     y + np.full(shape=len(y), fill_value=0.4),
                                     facecolor='white', alpha=0.95, zorder=3
                                     )
                    plh[patient_id].append(d_line)
                    plh[patient_id].append(c_marker)
                    plh[patient_id].append(crs_marker)
        ax.set_xticks(x)
        # ax.set_xticklabels(df.columns, rotation=90)
        ax.set_xticklabels(df.columns)
        classes_legend = plt.legend(handles=[mpatches.Patch(color=cmap(kls), label=kls) for kls in classes],
                                    shadow=True, fancybox=True, loc=1
                                    )
        plt.gca().add_artist(classes_legend)
        if patients is not None:
            patients_legend = plt.legend([tuple(plh[patient_id]) for patient_id in patients.keys()],
                                         [patients[patient_id]["full_name"] for patient_id in patients.keys()],
                                         shadow=True, fancybox=True, loc=2, title=class_col
                                         )
            plt.gca().add_artist(patients_legend)
        plt.grid()
        fig.savefig(out, format=img_format)
        return ax
