import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from apps.analytics.visualizers.base_visualizer import *


class CorrHeatMapVisualizer(Visualizer):
    def visualize(self, df, **kwargs):
        df = df.copy()

        # Output stream
        out = kwargs.get('out', self.out)

        # Class column
        class_col = kwargs.get('class_col', self.class_col)
        width = kwargs.get('width', self.width)
        height = kwargs.get('height', self.height)

        # Image format
        img_format = kwargs.get('format', self.img_format)

        col_count = len(df.columns) - 1
        classes = df[class_col].unique()
        cls_count = classes.shape[0]
        fig = plt.figure(figsize=(width * cls_count, height * col_count))
        i = 0
        for kls in classes:
            i += 1
            kls_df = df[df[class_col] == kls]
            correlations = kls_df.corr()
            ax = fig.add_subplot(cls_count, 1, i)
            cax = ax.matshow(correlations, cmap=cmx.jet, vmin=-1, vmax=1, interpolation='nearest')
            cb = fig.colorbar(cax, fraction=0.046, pad=0.04)
            cb.ax.tick_params(labelsize=12)
            cb.set_label('Corr')
            ticks = np.arange(0, col_count, 1)
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
            ax.xaxis.set_ticks_position('bottom')
            ax.set_xticklabels([col for col in df.columns if col != class_col], fontsize=12)
            ax.set_yticklabels([col for col in df.columns if col != class_col], fontsize=12)
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=90)
            plt.text(0.5, 1.17, kls,
                     horizontalalignment='center',
                     fontsize=21,
                     transform=ax.transAxes)
        # plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=10)
        plt.tight_layout()
        plt.savefig(out, format=img_format)
