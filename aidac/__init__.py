from aidac.dataframe.DataFrame import *
from aidac.dataframe.LocalTable import LocalTable
from aidac.dataframe.Scheduler import Scheduler
from aidac.data_source.DataSourceManager import *

__name__ = 'aidac'

ac = Scheduler()
manager = DataSourceManager()


def add_data_source(source: str, host: str, user: str, password: str, db: str, job_name: str = None, port: str = None):
    manager.add_data_source(source, host, user, password, db, job_name, port)


def data_sources():
    pass


def tables():
    manager.tables()


def read_csv(path, delimiter=None, header=None):
    return LocalTable.read_csv(path, delimiter, header)


def read_remote_data(job: str, table_name: str):
    """
    Create a remote table
    If job or table does not exist, an exception will be raised
    @param job: a data source
    @param table_name: remote table name
    @return:
    """
    source = manager.get_data_source(job)
    return RemoteTable(source, table_name=table_name)
