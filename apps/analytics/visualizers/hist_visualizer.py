import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
from apps.analytics.visualizers.base_visualizer import *


class HistVisualizer(Visualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bins = kwargs.get('bins', 60)

    def visualize(self, df, **kwargs):
        df = df.copy()

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        # Alpha
        alpha = kwargs.get('alpha', self.alpha)

        # Bins
        bins = kwargs.get('bins', self.bins)

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
        ax = fig.get_axes()
        classes = df[class_col].unique()
        i = 0
        for feature in features:
            i += 1
            fig.add_subplot(int(math.ceil(ftr_count / 2)), 2, i)
            for kls in classes:
                values = df[df[class_col] == kls][feature]
                mu = np.mean(values)
                sigma = np.std(values)
                n, bins, patches = plt.hist(values, bins=bins, normed=1, label=kls, alpha=alpha)
                y = mlab.normpdf(bins, mu, sigma)
                plt.gca().set_xlabel('Values')
                plt.gca().set_ylabel('Frequency')
                plt.title(feature)
            plt.legend(shadow=True, fancybox=True, loc=1, title=class_col)
        plt.tight_layout()
        plt.savefig(out, format=img_format)
        return ax
