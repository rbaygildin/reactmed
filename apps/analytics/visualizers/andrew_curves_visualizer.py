import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
from apps.analytics.visualizers.base_visualizer import *


class AndrewsCurvesVisualizer(Visualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_samples = kwargs.get('n_samples', 200)
        self.n_x_ticks = kwargs.get('n_x_ticks', 10)

    def visualize(self, df, **kwargs):

        def get_function(ampl):

            def func(t0):
                x1 = ampl[0]
                y = x1 / np.sqrt(2.0)
                coeff = np.delete(np.copy(ampl), 0)
                coeff.resize(int((coeff.size + 1) / 2), 2)

                harmonics = np.arange(0, coeff.shape[0]) + 1
                trg_args = np.outer(harmonics, t0)
                y += np.sum(
                    coeff[:, 0, np.newaxis] * np.sin(trg_args) + coeff[:, 1, np.newaxis] * np.cos(trg_args),
                    axis=0
                )
                return y

            return func

        df = df.copy()
        m = len(df)

        # Feature columns
        feature_cols = kwargs.get('feature_cols', self.feature_cols)

        # Class col
        class_col = kwargs.get('class_col', self.class_col)

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format (default 'png')
        img_format = kwargs.get('format', self.img_format)

        # Number of X points (default 10)
        n_samples = kwargs.get('n_samples', self.n_samples)

        # Alpha (default 1.0)
        alpha = kwargs.get('alpha', self.alpha)

        # Color map
        color_map = kwargs.get('color_map', self.color_map)

        # Figure size
        figsize = kwargs.get('figsize', self.figsize)

        # Number of X ticks
        n_x_ticks = kwargs.get('n_x_ticks', self.n_x_ticks)

        # Class column
        kls_df = df[class_col]

        # Get all classes
        classes = kls_df.drop_duplicates()

        # Delete class column
        df = df.drop(class_col, axis=1)

        # If feature columns were chosen we delete others from data frame
        if feature_cols is not None:
            chosen_cols = [col for col in feature_cols]
            df = df[chosen_cols]

        cmap = class_color(classes.values, color_map=color_map)
        norm = kwargs.get('norm', self.norm)
        if norm == 'scale':
            df = df.apply(scale)
        elif norm == 'center':
            df = df.apply(standardize)

        # Patients who need to be shown on the chart
        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {p["patient_id"]: p for p in patients.to_dict('records')}

        if patients is not None:
            p2cmap = class_color(list(patients.keys()), color_map=color_map, invert=True)

        # X
        t = np.linspace(-np.pi, np.pi, n_samples)

        # Start to draw chart
        fig = plt.figure(figsize=figsize)

        # Get current axes
        ax = fig.gca(xlim=[-np.pi, np.pi])

        # X ticks
        points = np.linspace(-np.pi, np.pi, n_x_ticks)

        # patient legend handles
        plh = {}

        for i in range(m):
            f = get_function(df.iloc[i].values)
            ac_series = f(t)
            ac_series_points = f(points)
            kls = kls_df.iat[i]
            patient = None
            if patients is not None:
                patient_id = df.index.values[i]
                patient = patients.get(patient_id, None)
            if patient is not None:
                plh[patient_id] = []
                # white line
                w_line, = plt.plot(t, ac_series, c='white', linewidth=4, zorder=3)
                # dashed line
                d_line, = plt.plot(t, ac_series, c=cmap(kls), alpha=1.0, linewidth=4, linestyle='--', zorder=4)
                # circle
                c_marker, = plt.plot(points, ac_series_points, 'o', c=p2cmap(patient_id), zorder=5, markersize=16)
                # cross
                crs_marker, = plt.plot(points, ac_series_points, 'x', c='white', zorder=6, markersize=10,
                                       markeredgewidth=2)
                plh[patient_id].append(w_line)
                plh[patient_id].append(d_line)
                plh[patient_id].append(c_marker)
                plh[patient_id].append(crs_marker)
            else:
                plt.plot(t, f(t), c=cmap(kls), alpha=alpha)

        classes_legend = plt.legend(title=class_col,
                                    handles=[mpatches.Patch(color=cmap(kls), label=kls) for kls in classes],
                                    shadow=True, fancybox=True, loc=1)
        ax.add_artist(classes_legend)
        if patients is not None:
            patients_legend = plt.legend([tuple(plh[patient_id]) for patient_id in patients.keys()],
                                         [patients[patient_id]["full_name"] for patient_id in patients.keys()],
                                         shadow=True, fancybox=True, loc=2, title="Пациенты")
            ax.add_artist(patients_legend)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid()
        t1 = time.time()
        fig.savefig(out, format=img_format)
        t2 = time.time()
        print("Andrews Curves Save Figure: %f" % ((t2 - t1) * 1000))
        return ax
