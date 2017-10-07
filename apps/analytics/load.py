import numpy as np
from pandas import pivot_table, DataFrame

from apps.analytics.etl import PostgresDataLoader


def scale(series):
    a = min(series)
    b = max(series)
    return (series - a) / (b - a)


def standardize(series):
    mean = np.mean(series)
    std = np.std(series)
    return (series - mean) / std


def data_load(**kwargs):
    load_pattern = kwargs.get('load_pattern', 'fc')
    test = kwargs.get('test')
    feature_cols = kwargs.get('feature_cols')
    class_col = kwargs.get('class_col')
    normalize = kwargs.get("normalize", None)
    if load_pattern == 'fc':
        df = PostgresDataLoader.load_data(test=test, features=feature_cols, classes=class_col, load_pattern='fc')
        if df is None or len(df) == 0:
            raise ValueError('Система вернула пустой датасет. Убедитесь, что вы правильно ввели параметры.')
        class_col = df.iloc[0]['class_column']
        kls_df = {
            class_col: df['class'].tolist()
        }
        _classes_df = DataFrame(data=kls_df, index=df['patient_id'].tolist())
        del df['class']
        del df['class_column']
        df = pivot_table(data=df,
                         index=['patient_id'],
                         values=['feature_value'],
                         columns=['feature']
                         )
        df.columns = df.columns.get_level_values(1)
        if normalize == "scale":
            df = df.apply(scale)
        elif normalize == "std":
            df = df.apply(standardize)
        df = df.join(_classes_df).drop_duplicates()
        return df, class_col
    elif load_pattern == 'f':
        df = PostgresDataLoader.load_data(test=test, features=feature_cols, load_pattern='f')
        if df is None or len(df) == 0:
            raise ValueError('Система вернула пустой датасет. Убедитесь, что вы правильно ввели параметры.')
        df = pivot_table(data=df,
                         index=['patient_id'],
                         values=['feature_value'],
                         columns=['feature']
                         )
        df.columns = df.columns.get_level_values(1)
        if normalize == "scale":
            df = df.apply(scale)
        elif normalize == "std":
            df = df.apply(standardize)
        return df, None
    return None
