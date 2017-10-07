from abc import abstractmethod

import matplotlib

matplotlib.use('Agg')

import matplotlib.cm as cmx
import matplotlib.colors as colors
import numpy as np


def class_color(classes, color_map='brg', invert=False):
    n_kls = len(classes)
    color_norm = colors.Normalize(vmin=0, vmax=n_kls)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=color_map)
    if invert:
        indexes = list(reversed(range(0, n_kls)))
    else:
        indexes = list(range(0, n_kls))
    cmap = dict(zip(classes, indexes))

    def get_kls_color(kls):
        return scalar_map.to_rgba(cmap[kls])

    return get_kls_color


def scale(series):
    a = min(series)
    b = max(series)
    return (series - a) / (b - a)


def standardize(series):
    mu = np.mean(series)
    sigma = np.std(series)
    return (series - mu) / sigma


class Visualizer:
    def __init__(self, **kwargs):
        self.alpha = kwargs.get('alpha', 1.0)
        self.out = kwargs.get('out', None)
        self.img_format = kwargs.get('format', 'png')
        self.color_map = kwargs.get('color_map', 'brg')
        self.width = kwargs.get('width', 12)
        self.height = kwargs.get('height', 8)
        self.figsize = kwargs.get('figsize', (self.width, self.height))
        self.feature_cols = kwargs.get('feature_cols', None)
        self.class_col = kwargs.get('class_col', None)
        self.patients = kwargs.get('patients', None)
        self.norm = kwargs.get('norm', 'none')

    @abstractmethod
    def visualize(self, data, **kwargs):
        pass
