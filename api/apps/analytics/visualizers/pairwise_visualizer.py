import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.ticker import NullFormatter

from apps.analytics.visualizers.base_visualizer import *


class PairWiseVisualizer(Visualizer):
    def __init__(self, **kwargs):
        feature_cols = kwargs.get('feature_cols', [])
        self.feature1 = feature_cols[0]
        self.feature2 = feature_cols[1]
        self.reg_type = kwargs.get('reg_type', 'linear')
        self.degree = kwargs.get('degree', 2)
        super().__init__(**kwargs)

    def visualize(self, df, **kwargs):
        df = df.copy()

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        # Alpha
        alpha = kwargs.get('alpha', self.alpha)

        # Figure size
        figsize = kwargs.get('figsize', self.figsize)

        # Class column
        class_col = kwargs.get('class_col', self.class_col)

        classes = df[class_col].drop_duplicates().values

        # First feature
        feature1 = kwargs.get('feature1', self.feature1)

        # Second feature
        feature2 = kwargs.get('feature2', self.feature2)

        # Regression
        reg_type = kwargs.get('reg_type', self.reg_type)

        # Degree
        degree = kwargs.get('degree', self.degree)

        # Color map
        color_map = kwargs.get('color_map', self.color_map)
        cmap = class_color(classes, color_map=color_map)

        # Patients
        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {p['patient_id']: p for p in patients.to_dict('records')}
        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        bottom_h = left_h = left + width + 0.02

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom_h, width, 0.2]
        rect_histy = [left_h, bottom, 0.2, height]

        figsize = kwargs.get('figsize', (self.width, self.height))
        fig = plt.figure(figsize=figsize)

        ax_scatter = plt.axes(rect_scatter)
        ax_histx = plt.axes(rect_histx)
        ax_histy = plt.axes(rect_histy)

        nullfmt = NullFormatter()
        # no labels
        ax_histx.xaxis.set_major_formatter(nullfmt)
        ax_histy.yaxis.set_major_formatter(nullfmt)

        # if feature1 is not None and feature2 is not None:
        #     df = df[[feature1, feature2, class_col]]
        for kls in classes:
            kls_df = df[df[class_col] == kls]
            # i2p_id = {kls_df.index.get_loc(p_id): p_id for p_id in kls_df.index.values}
            del kls_df[class_col]
            m = kls_df.shape[0]
            points, = ax_scatter.plot(kls_df[kls_df.columns[0]], kls_df[kls_df.columns[1]], 'o', label=kls, alpha=alpha, c=cmap(kls))
            kls_color = points.get_color()
            for i in range(m):
                if patients is not None:
                    p_id = kls_df.index[i]
                    patient = patients.get(p_id, None)
                    if patient is not None:
                        ax_scatter.plot(kls_df.iloc[i, 0], kls_df.iloc[i, 1], '8', c=kls_color, zorder=5, markersize=16,
                                        markeredgecolor='black', markeredgewidth=2)
                        ax_scatter.plot(kls_df.iloc[i, 0], kls_df.iloc[i, 1], 'x', c='black', zorder=6, markersize=8,
                                        markeredgewidth=1)
                        ax_scatter.annotate(patient['full_name'], xy=(kls_df.iloc[i, 0], kls_df.iloc[i, 1]),
                                            xycoords='data',
                                            xytext=(-40, 40), textcoords='offset points', ha='right',
                                            va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                                            arrowprops=dict(facecolor='black'),
                                            zorder=7
                                            )
        del df[class_col]
        X = df[df.columns[0]].reshape((-1, 1))
        Y = df[df.columns[1]]
        if reg_type == 'linear':
            sample_size = df.shape[0]
            reg = LinearRegression()
            reg.fit(X, Y)
            r2 = reg.score(X, Y)
            slope = np.degrees(np.arctan(r2))
            print("Linear regression R^2 Score = %f" % r2)
            n_points = 50
            x_min = np.min(X)
            x_max = np.max(X)
            x = np.linspace(x_min, x_max, n_points)
            # x_step = (x_max - x_min) / n_points
            y_predict = reg.predict(x.reshape(-1, 1))
            y_min = np.min(y_predict)
            y_max = np.max(y_predict)
            # y_step = (y_max - y_min) / n_points
            ax_scatter.plot(x, y_predict, c='black', linewidth=3)
            x_med = (x_max + x_min) / 2
            y_med = (y_max + y_min) / 2
            # slope = np.degrees(np.arctan(y_step / x_step))
            ax_scatter.annotate("R^2=%.2f" % r2, xy=(x_med, y_med), xytext=(x_med, y_med + 0.5), rotation=slope,
                                fontsize=12)
        elif reg_type == 'poly':
            sample_size = df.shape[0]
            reg = make_pipeline(PolynomialFeatures(degree), Ridge())
            reg.fit(X, Y)
            r2 = reg.score(X, Y)
            slope = np.degrees(np.arctan(r2))
            print("Nonlinear regression R^2 Score = %f" % r2)
            x_min = np.min(X)
            x_max = np.max(X)
            x = np.linspace(x_min, x_max, 50)
            y_predict = reg.predict(x.reshape(-1, 1))
            y_min = np.min(y_predict)
            y_max = np.max(y_predict)
            ax_scatter.plot(x, y_predict, c='black', linewidth=3)
            x_med = (x_max + x_min) / 2
            y_med = (y_max + y_min) / 2
            ax_scatter.annotate("R^2=%.2f" % r2, xy=(x_med, y_med), xytext=(x_med, y_med + 0.5), rotation=slope + 5,
                                fontsize=12)
        ax_scatter.set_xlabel(df.columns.values[0])
        ax_scatter.set_ylabel(df.columns.values[1])
        ax_scatter.legend(title=class_col, handles=[mpatches.Patch(color=cmap(kls), label=kls) for kls in classes],
                          shadow=True, fancybox=True, loc=1)
        ax_histx.hist(df[df.columns[0]].values, bins=60)
        ax_histy.hist(df[df.columns[1]].values, bins=60, orientation='horizontal')

        ax_histx.set_xlim(ax_scatter.get_xlim())
        ax_histy.set_ylim(ax_scatter.get_ylim())
        fig.savefig(out, format=img_format)
