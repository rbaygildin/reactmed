import numpy as np
from pandas import DataFrame

from apps.core.models import TestRec


def scale(series):
    a = min(series)
    b = max(series)
    return (series - a) / (b - a)


def standardize(series):
    mean = np.mean(series)
    std = np.std(series)
    return (series - mean) / std


def rec_to_row(class_col=None, feature_cols=None):
    def mapper(rec):
        row = {}
        for ind_id, ind in rec['real_inds'].items():
            if feature_cols is not None and ind_id in feature_cols:
                continue
            row[rec['real_inds'][ind_id]['name']] = ind['value']
        row['patient_id'] = rec['patient_id']
        if class_col is not None:
            row[rec['text_inds'][class_col]['name']] = rec['text_inds'][class_col]['value']
        return row

    return mapper


def data_load(**kwargs):
    test = kwargs.get('test')
    feature_cols = kwargs.get('feature_cols', None)
    class_col = kwargs.get('class_col', None)
    normalize = kwargs.get("normalize", None)
    test_recs = TestRec.objects.filter(short_name=test).values()
    if len(test_recs) <= 0:
        raise ValueError('Система вернула пустой датасет. Убедитесь, что вы правильно ввели параметры.')
    df = list(map(rec_to_row(class_col=class_col, feature_cols=feature_cols), test_recs))
    df = DataFrame(data=df)
    df.set_index(['patient_id'], drop=True, inplace=True)
    kls_df = None
    if class_col is not None:
        class_col = test_recs[0]['text_inds'][class_col]['name']
        kls_df = df[class_col]
        del df[class_col]
    if normalize == "scale":
        df = df.apply(scale)
    elif normalize == "std":
        df = df.apply(standardize)
    if class_col is not None:
        df[class_col] = kls_df
    return df, class_col
