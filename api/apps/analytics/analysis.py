from abc import abstractmethod

import numpy as np
import pandas as pd
import scipy.stats as sts
import sklearn.decomposition as decom
import sklearn.linear_model as lm
import sklearn.preprocessing as prep
from sklearn.feature_selection import RFE, SelectKBest, chi2, f_classif
from sklearn.linear_model import LogisticRegression


class DataAnalyser:
    @abstractmethod
    def perform_analysis(self, df, **kwargs):
        pass


class DescriptiveStatAnalyser(DataAnalyser):
    def perform_analysis(self, df, **kwargs):
        classes = kwargs.get("class_col", None)
        features = kwargs.get("feature_cols", None)
        stat = {}
        for col in df.columns:
            if not col == classes:
                stat[col] = {}
                stat[col]["Средняя"] = df[col].mean()
                stat[col]["Стд. квад. отклонение"] = df[col].std()
                stat[col]["Объем выборки"] = df[col].count()
                stat[col]["Минимум"] = df[col].min()
                stat[col]["Максимум"] = df[col].max()
                stat[col]["Дов. интервал 95%"] = sts.norm.interval(.95, loc=stat[col]["Средняя"],
                                                                   scale=stat[col]["Стд. квад. отклонение"])
                stat[col]["Дов. интервал 90%"] = sts.norm.interval(.90, loc=stat[col]["Средняя"],
                                                                   scale=stat[col]["Стд. квад. отклонение"])
                stat[col]["Квантиль 25%"] = df[col].quantile(.25)
                stat[col]["Квантиль 50%"] = df[col].quantile(.5)
                stat[col]["Квантиль 75%"] = df[col].quantile(.75)
                stat[col]["Мода"] = df[col].mode().tolist()
        return pd.DataFrame.from_dict(stat)


class LinearRegressionAnalyser(DataAnalyser):
    def perform_analysis(self, df, **kwargs):
        y_col = kwargs.get("y_col", None)
        y = df[y_col]
        del df[y]
        x = df
        reg_model = lm.LinearRegression(fit_intercept=True, normalize=True)
        reg_model.fit(x, y)
        return reg_model, {
            "coef": reg_model.coef_,
            "intercept": reg_model.intercept_
        }


class FeaturesSelectionAnalyser(DataAnalyser):
    def perform_analysis(self, df, **kwargs):

        def scale(series):
            a = np.min(series)
            b = np.max(series)
            return (series - a) / (b - a)

        def standardize(series):
            mean = np.mean(series)
            std = np.std(series)
            return (series - mean) / std

        df_temp = df.copy()
        class_col = kwargs.get('class_col', None)
        normalize = kwargs.get('normalize', 'scale')
        select_method = kwargs.get('select_method', 'logit')
        if select_method == 'logit':
            if class_col is None:
                raise ValueError("Категориальная переменная не была задана!")
            kls_df = df_temp[class_col].to_frame()
            del df_temp[class_col]
            n_cols = len(df_temp.columns)
            n_features = kwargs.get('n_features', n_cols // 2)
            if n_features > n_cols:
                raise ValueError("Количество отбираемых переменных "
                                 "не может быть больше количества переменных в исходной выборке")
            if n_features <= 0:
                raise ValueError("Количество отбираемых переменных не может быть неположительным числом!")
            if normalize == 'scale':
                df_temp = df_temp.apply(scale)
            elif normalize == 'std':
                df_temp = df_temp.apply(standardize)
            x = df_temp
            y = np.ravel(kls_df)
            model = LogisticRegression()
            rfe = RFE(model, n_features)
            rfe.fit(x, y)
            col_ranks = [(df.columns.values[i], rank) for i, rank in enumerate(rfe.ranking_)]
            col_ranks.sort(key=lambda tup: tup[1])
            df_temp = df[[col[0] for col in col_ranks[0:n_features]]]
            df_temp[class_col] = kls_df
            return df_temp
        elif select_method == 'pca':
            index = df_temp.index
            kls_df = None
            if class_col is not None:
                kls_df = df_temp[class_col].to_frame()
                del df_temp[class_col]
            n_cols = len(df_temp.columns)
            n_features = kwargs.get('n_features', n_cols // 2)
            if n_features > n_cols:
                raise ValueError("Количество отбираемых переменных "
                                 "не может быть больше количества переменных в исходной выборке")
            if n_features <= 0:
                raise ValueError("Количество отбираемых переменных не может быть неположительным числом!")
            pca = decom.PCA(n_components=n_features)
            df_temp = df_temp.apply(standardize)
            if class_col is not None:
                pca.fit(df_temp, kls_df)
            else:
                pca.fit(df_temp)
            df_temp = pca.transform(df_temp)
            df_temp = pd.DataFrame(df_temp, index=index, columns=["PCA %d" % i for i in range(1, n_features + 1)])
            if class_col is not None:
                df_temp[class_col] = kls_df
            return df_temp
        else:
            return df


class ImputerAnalyser(DataAnalyser):
    def perform_analysis(self, df, **kwargs):
        df = df.copy()
        index = df.index
        class_col = kwargs.get('class_col', None)
        strategy = kwargs.get('strategy', 'mean')
        if class_col is not None:
            kls_df = df[class_col]
            df = df.drop(class_col, axis=1)
            cols = df.columns
            imputer = prep.Imputer(strategy=strategy)
            imputer.fit(df)
            df = imputer.transform(df)
            df = pd.DataFrame(data=df, columns=cols, index=index)
            df[class_col] = kls_df
        else:
            cols = df.columns
            imputer = prep.Imputer(strategy=strategy)
            imputer.fit(df)
            df = imputer.transform(df)
            df = pd.DataFrame(data=df, columns=cols, index=index)
        return df
