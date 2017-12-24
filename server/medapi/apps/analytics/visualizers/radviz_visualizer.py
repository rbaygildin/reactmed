import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from apps.analytics.visualizers.base_visualizer import *


class RadVizVisualizer(Visualizer):
    def visualize(self, df, **kwargs):

        m = len(df)

        # Feature columns
        feature_cols = kwargs.get('feature_cols', self.feature_cols)

        # Class col
        class_col = kwargs.get('class_col', self.class_col)

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format (default 'png')
        img_format = kwargs.get('format', self.img_format)

        # Alpha (default 1.0)
        alpha = kwargs.get('alpha', self.alpha)

        # Figure size
        figsize = kwargs.get('figsize', self.figsize)

        # Class column
        kls_df = df[class_col]

        # Get all classes
        classes = kls_df.drop_duplicates()

        # Color map
        color_map = kwargs.get('color_map', self.color_map)
        cmap = class_color(classes, color_map=color_map)

        # Delete class column
        df = df.drop(class_col, axis=1).apply(scale)

        # If feature columns were chosen we delete others from data frame
        if feature_cols is not None:
            df = df[[col for col in feature_cols]]

        patients = kwargs.get('patients', self.patients)

        if isinstance(patients, pd.DataFrame):
            patients = {df.index.get_loc(p['patient_id']): p for p in patients.to_dict('records')}

        fig = plt.figure(figsize=figsize)
        k = 1
        ax = plt.gca(xlim=[-k, k], ylim=[-k, k])
        m = len(df)
        n_cols = len(df.columns)
        n = n_cols
        s = np.array([(k * np.cos(t), k * np.sin(t))
                      for t in [2.0 * np.pi * (i / float(n))
                                for i in range(n)]])
        for i in range(m):
            row = df.iloc[i].values
            row_ = np.repeat(np.expand_dims(row, axis=1), 2, axis=1)
            y = (s * row_).sum(axis=0) / row.sum()
            kls = kls_df.iat[i]
            kls_color = cmap(kls)
            plt.scatter(y[0], y[1], label=kls, c=kls_color, alpha=alpha)
            if patients is not None:
                patient_id = df.index.values[i]
                patient = patients.get(patient_id, None)
                if patient is not None:
                    plt.plot(y[0], y[1], 'o', c=kls_color, zorder=5, markersize=18, markeredgecolor='white',
                             markeredgewidth=1.5)
                    plt.plot(y[0], y[1], 'x', c='white', zorder=6, markersize=11, markeredgewidth=1.5)
                    ax.annotate(patient['full_name'], xy=(y[0] - 0.02, y[1] + 0.03), xycoords='data',
                                xytext=(-40, 40), textcoords='offset points', ha='right',
                                va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                                arrowprops=dict(facecolor='black', width=1),
                                zorder=7
                                )
        ax.add_patch(mpatches.Circle((0.0, 0.0), radius=1.0, edgecolor='gray', facecolor='none'))
        for sxy, col_name in zip(s, df.columns):
            ax.add_patch(mpatches.Circle(sxy, radius=0.025, facecolor='gray'))
            #             ax.add_line(mlines.Line2D((0.0, sxy[0]), (0.0, sxy[1]), lw=1., alpha=0.2, c='grey'))
            if sxy[0] < 0.0 and sxy[1] < 0.0:
                ax.text(sxy[0] - 0.025, sxy[1] - 0.025, col_name,
                        ha='right', va='top', size='small')
            elif sxy[0] < 0.0 <= sxy[1]:
                ax.text(sxy[0] - 0.025, sxy[1] + 0.025, col_name,
                        ha='right', va='bottom', size='small')
            elif sxy[0] >= 0.0 > sxy[1]:
                ax.text(sxy[0] + 0.025, sxy[1] - 0.025, col_name,
                        ha='left', va='top', size='small')
            elif sxy[0] >= 0.0 and sxy[1] >= 0.0:
                ax.text(sxy[0] + 0.025, sxy[1] + 0.025, col_name,
                        ha='left', va='bottom', size='small')
        classes_legend = plt.legend(handles=[mpatches.Patch(color=cmap(kls), label=kls) for kls in classes],
                                    shadow=True, fancybox=True, loc=1, title=class_col
                                    )
        ax.add_artist(classes_legend)
        plt.grid(linewidth=1, c='gray', alpha=0.1)
        plt.xlabel('X')
        plt.ylabel('Y')
        ax.axis('equal')
        fig.savefig(out, format=img_format)
        return ax
