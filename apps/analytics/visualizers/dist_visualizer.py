import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math
from sklearn.neighbors import KernelDensity
from apps.analytics.visualizers.base_visualizer import *


class DistVisualizer(Visualizer):
    def visualize(self, df, **kwargs):
        df = df.copy()

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        # Alpha
        alpha = kwargs.get('alpha', self.alpha)

        # Class column
        class_col = kwargs.get('class_col', self.class_col)

        features = [col for col in df.columns if col != class_col]
        ftr_count = len(features)
        w_unit = 6
        h_unit = 5
        # w = w_unit * int(math.ceil(ftr_count / 2))
        w = w_unit * 2
        h = h_unit * int(math.ceil(ftr_count / 2))
        fig = plt.figure(figsize=(w, h))
        classes = df[class_col].unique()
        cmap = class_color(classes)
        i = 0
        for feature in features:
            i += 1
            ftr_min = df[feature].min()
            ftr_max = df[feature].max()
            rng = ftr_max - ftr_min
            step = rng / 100
            ftr_min -= 40 * step
            ftr_max += 40 * step
            xs = np.linspace(ftr_min, ftr_max, num=100)
            ax = fig.add_subplot(int(math.ceil(ftr_count / 2)), 2, i)
            for kls in classes:
                values = df[df[class_col] == kls][feature].as_matrix()
                kde = KernelDensity(kernel='gaussian', bandwidth=0.4).fit(values.reshape(-1, 1))
                dens = np.exp(kde.score_samples(xs.reshape(-1, 1)))
                plt.plot(xs, dens, label=kls, alpha=0.7, c=cmap(kls))
                plt.fill_between(xs, np.full((100), 0.0), dens, facecolor=cmap(kls), interpolate=True, alpha=alpha)
                ax.set_xlabel('Values')
                ax.set_ylabel('Density')
                plt.title(feature)
            plt.legend(shadow=True, fancybox=True, loc=1, title=class_col)
            plt.grid(linewidth=1, c='gray', alpha=0.2)
        plt.tight_layout()
        plt.savefig(out, format=img_format)
        return ax
