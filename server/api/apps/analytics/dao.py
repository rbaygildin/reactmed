import psycopg2 as pg
from psycopg2.extras import DictCursor
from abc import abstractmethod

from apps.analytics.query import Query

dbname = "laksmimed_db"
user = "laksmimed_user"
password = "laksmimed95root"
conn_str = "dbname=%s user=%s password=%s" % (dbname, user, password)


class IDatasetDao:
    @abstractmethod
    def create_dataset(self, dataset):
        pass

    @abstractmethod
    def find_datasets(self):
        pass

    @abstractmethod
    def update_dataset(self, dataset):
        pass

    @abstractmethod
    def delete_dataset(self, dataset_id):
        pass


class DatasetDao(IDatasetDao):
    def create_dataset(self, dataset):
        conn = pg.connect(conn_str, cursor_factory=DictCursor)
        cur = conn.cursor()
        q = Query.construct(dialect='postgres')
        q = q.table('datasets').save(**dataset)
        cur.execute(str(q))

    def find_datasets(self):
        conn = pg.connect(conn_str, cursor_factory=DictCursor)
        cur = conn.cursor()
        q = Query.construct(dialect='postgres')
        q = q.table('datasets').find()
        cur.execute(str(q))
        datasets = []
        for row in q.fetchall():
            datasets.append(dict(row))
        return datasets

    def update_dataset(self, dataset):
        conn = pg.connect(conn_str, cursor_factory=DictCursor)
        cur = conn.cursor()
        q = Query.construct(dialect='postgres')
        dataset_id = dataset["dataset_id"]
        del dataset["dataset_id"]
        q = q.table('datasets').update(**dataset).where("dataset_id = %d" % dataset_id)
        cur.execute(str(q))

    def delete_dataset(self, dataset_id):
        conn = pg.connect(conn_str, cursor_factory=DictCursor)
        cur = conn.cursor()
        q = Query.construct(dialect='postgres')
        q = q.table('datasets').delete().where('dataset_id = %d' % dataset_id)
        cur.execute(str(q))
