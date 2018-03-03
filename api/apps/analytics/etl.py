from abc import abstractmethod
from pandas import read_sql, read_csv
import psycopg2 as pg
from collections import Iterable


class DataLoader:
    @classmethod
    @abstractmethod
    def configure_data_source(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def load_data(cls, **kwargs):
        pass


class PostgresDataLoader(DataLoader):
    conn_str = ''

    @classmethod
    def load_data(cls, **kwargs):
        query = kwargs.get('query', None)
        test = kwargs.get('test', '')
        features = kwargs.get('features', [])
        classes = kwargs.get('classes', '')
        limit = kwargs.get('limit', None)
        offset = kwargs.get('offset', None)
        load_pattern = kwargs.get("load_pattern", "f")
        gen_q = 'SELECT '
        if query is None:
            if load_pattern == "fc":
                gen_q += 'tr1.patient_id patient_id, f1.value feature_value, f_meta1.name feature, c1.value "class", ' \
                         'c_meta1.name class_column '
                gen_q += 'FROM real_indicator_records f1, ' \
                         'test_records tr1, ' \
                         'text_indicator_records c1, ' \
                         'real_indicators f_meta1, ' \
                         'text_indicators c_meta1 '
                gen_q += "WHERE f1.test_record_id = tr1.test_record_id " \
                         "AND c1.test_record_id = tr1.test_record_id " \
                         "AND f1.indicator_id = f_meta1.indicator_id " \
                         "AND c1.indicator_id = c_meta1.indicator_id " \
                         "AND c1.indicator_id = '%s' " % classes
                gen_q += "AND tr1.test_id = '%s' " % test
                if isinstance(features, Iterable) and len(features) > 0:
                    features = map(lambda f: "'%s'" % f, features)
                    gen_q += ' AND f_meta1.indicator_id IN (' + ', '.join(features) + ') '
            elif load_pattern == "f":
                gen_q += 'tr1.patient_id patient_id, f1.value feature_value, f_meta1.name feature '
                gen_q += 'FROM real_indicator_records f1, ' \
                         'test_records tr1, ' \
                         'real_indicators f_meta1 '
                gen_q += "WHERE f1.test_record_id = tr1.test_record_id " \
                         "AND f1.test_record_id = tr1.test_record_id " \
                         "AND f1.indicator_id = f_meta1.indicator_id "
                gen_q += "AND tr1.test_id = '%s' " % test
                if isinstance(features, Iterable) and len(features) > 0:
                    features = map(lambda f: "'%s'" % f, features)
                    gen_q += ' AND f_meta1.indicator_id IN (' + ', '.join(features) + ') '
        else:
            return read_sql(query, pg.connect(cls.conn_str))
        print(gen_q)
        return read_sql(gen_q, pg.connect(cls.conn_str))

    @classmethod
    def configure_data_source(cls, **kwargs):
        dbname = kwargs.get('dbname', '')
        user = kwargs.get('user', '')
        password = kwargs.get('password', '')
        host = kwargs.get('host', 'localhost')
        cls.conn_str = 'dbname = %s user = %s password = %s host = %s' \
                       % (dbname, user, password, host)


class CSVDataLoader(DataLoader):
    @classmethod
    def load_data(cls, **kwargs):
        path = kwargs.get('path')
        sep = kwargs.get('sep', ',')
        return read_csv(path, sep=sep)

    @classmethod
    def configure_data_source(cls, **kwargs):
        pass
