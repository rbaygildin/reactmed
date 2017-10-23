import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math

from apps.analytics.visualizers.base_visualizer import *


class BoxplotVisualizer(Visualizer):
    def visualize(self, df, **kwargs):
        df = df.copy()

        # Class column
        classes_column = kwargs.get('class_col', self.class_col)

        # Output stream
        out = kwargs.get('out', self.out)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        w = 12
        h = 4 * int(math.ceil(len(df.columns) / 3))
        figsize = kwargs.get('figsize', (w, h))
        del df[classes_column]
        df.reset_index()
        ax = plt.gca()
        df.plot(kind='box', subplots=True, layout=(int(math.ceil(len(df.columns) / 3)), 3),
                sharex=False, sharey=False, figsize=figsize)
        # plt.tight_layout()
        plt.savefig(out, format=img_format)
        return ax
