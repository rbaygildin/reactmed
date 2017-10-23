import datetime
from enum import Enum

from abc import abstractmethod


class Query:

    def __init__(self, **kwargs):
        self.q = ''
        self.tb = ''

    @staticmethod
    def construct(**kwargs):
        if kwargs['dialect'] is None:
            raise ValueError('SQL dialect is not defined!')
        if kwargs['dialect'] == SQLDialect.postgres:
            return PostgresQuery(**kwargs)

    def table(self, tb):
        self.tb = tb
        return self

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def drop(self):
        pass

    @abstractmethod
    def save(self, **kwargs):
        pass

    @abstractmethod
    def save_if_not_exists(self, cond, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def find(self, *args):
        pass

    @abstractmethod
    def where(self, condition):
        pass

    @abstractmethod
    def and_where(self, condition):
        pass

    @abstractmethod
    def or_where(self, condition):
        pass

    @abstractmethod
    def limit(self, limit):
        pass

    @abstractmethod
    def returning(self, col):
        pass

    @abstractmethod
    def call(self, procedure):
        pass

    @abstractmethod
    def join(self, other, on):
        pass

    @abstractmethod
    def left_join(self, other, on):
        pass

    @abstractmethod
    def right_join(self, other, on):
        pass

    @abstractmethod
    def full_join(self, other, on):
        pass

    @abstractmethod
    def cross_join(self, other, on):
        pass

    def comma(self):
        self.q += ';'
        return self

    def raw(self, q):
        self.q = q
        return self

    def clear(self):
        self.q = ''
        return self

    def v2s(self, v):
        if isinstance(v, int):
            return "{}".format(v)
        elif isinstance(v, float):
            return "{}".format(v)
        elif isinstance(v, str):
            return "'{}'".format(v)
        elif isinstance(v, datetime.date):
            return "'{}'::date".format(v)
        elif isinstance(v, datetime.datetime):
            return "'{}'::timestamp".format(v)
        elif isinstance(v, list):
            return "'" + self.l2s(v) + "'"
        elif v is None:
            return "NULL"
        else:
            return str(v)

    def le2s(self, v):
        if isinstance(v, int):
            return "{}".format(v)
        elif isinstance(v, float):
            return "{}".format(v)
        elif isinstance(v, str):
            return '"{}"'.format(v)
        elif isinstance(v, datetime.date):
            return "'{}'::date".format(v)
        elif isinstance(v, datetime.datetime):
            return "'{}'::timestamp".format(v)
        elif isinstance(v, list):
            return self.l2s(v)
        elif v is None:
            return "NULL"
        else:
            return str(v)

    def l2s(self, l):
        r = '{'
        r += ', '.join([self.le2s(le) for le in l])
        r += '}'
        return r

    def __str__(self):
        return self.q


class PostgresQuery(Query):

    def create(self, **kwargs):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'CREATE TABLE {} '.format(self.tb)
        self.q += '({})'.format(', '.join(['{0} {1}'.format(cn, ct) for cn, ct in kwargs.items()]))
        return self

    def drop(self):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'DROP TABLE {}'.format(self.tb)
        return self

    def save(self, **kwargs):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'INSERT INTO {}'.format(self.tb)
        self.q += ' ({})'.format(', '.join(kwargs.keys()))
        self.q += ' VALUES ({})'.format(', '.join([self.v2s(v) for v in kwargs.values()]))
        return self

    def save_if_not_exists(self, cond, **kwargs):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'INSERT INTO {}'.format(self.tb)
        self.q += ' ({})'.format(', '.join(kwargs.keys()))
        self.q += ' SELECT {}'.format(', '.join([self.v2s(v) for v in kwargs.values()]))
        self.q += ' WHERE NOT EXISTS (SELECT 1 FROM {0} WHERE {1})'.format(self.tb, cond)
        return self

    def update(self, **kwargs):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'UPDATE {}'.format(self.tb)
        self.q += ' SET {}'.format(', '.join(['{0}={1}'.format(c, self.v2s(v)) for c, v in kwargs.items()]))
        return self

    def delete(self):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'DELETE FROM {}'.format(self.tb)
        return self

    def find(self, *args):
        if self.tb is None:
            raise ValueError('Table not defined!')
        if args is None or len(args) == 0:
            self.q = 'SELECT * FROM {}'.format(self.tb)
        else:
            self.q = 'SELECT {0} FROM {1}'.format(', '.join(args), self.tb)
        return self

    def where(self, condition):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' WHERE {}'.format(condition)
        return self

    def or_where(self, condition):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' AND {}'.format(condition)
        return self

    def and_where(self, condition):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' OR {}'.format(condition)
        return self

    def limit(self, limit):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' LIMIT {}'.format(limit)
        return self

    def returning(self, col):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' RETURNING {}'.format(col)
        return self

    def call(self, procedure):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q = 'CALL {}()'.format(procedure)
        return self

    def full_join(self, other, on):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' FULL OUTER JOIN {}'.format(other)
        self.q += ' ON {}'.format(' AND '.join(
            ['{0}.{1} = {2}.{3}'.format(self.tb, fc, other, sc) for fc, sc in on.items()
             ]))
        return self

    def left_join(self, other, on):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' LEFT OUTER JOIN {}'.format(other)
        self.q += ' ON {}'.format(' AND '.join(
            ['{0}.{1} = {2}.{3}'.format(self.tb, fc, other, sc) for fc, sc in on.items()
             ]))
        return self

    def join(self, other, on):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' INNER JOIN {}'.format(other)
        self.q += ' ON {}'.format(' AND '.join(
            ['{0}.{1} = {2}.{3}'.format(self.tb, fc, other, sc) for fc, sc in on.items()
             ]))
        return self

    def right_join(self, other, on):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' RIGHT OUTER JOIN {}'.format(other)
        self.q += ' ON {}'.format(' AND '.join(
            ['{0}.{1} = {2}.{3}'.format(self.tb, fc, other, sc) for fc, sc in on.items()
             ]))
        return self

    def cross_join(self, other, on):
        if self.tb is None:
            raise ValueError('Table not defined!')
        self.q += ' CROSS JOIN {}'.format(other)
        self.q += ' ON {}'.format(' AND '.join(
            ['{0}.{1} = {2}.{3}'.format(self.tb, fc, other, sc) for fc, sc in on.items()
             ]))
        return self


class ConnFactory:

    @abstractmethod
    def connect(self, conn_s):
        pass

    @abstractmethod
    def cursor(self, conn):
        pass


class SQLDialect(Enum):
    mysql = 'mysql'
    postgres = 'postgres'
    oracle = 'oracle'
    mssql = 'mssql'
    sqlite = 'sqlite'