import os
import sys
import sqlite3
from time import time;
from sqlite3 import Error

import logging

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class MainSQL(object):
    def __init__(self, dbname:str = None) -> None:
        if dbname is None:
            raise Exception("No dbname in EnergiePrijzen")

        self.__dbname = dbname
        self._conn = None
        pass

    def _connection(self)->None:
        """ create a database connection to a SQLite database """
        try:
            self._conn = sqlite3.connect(self.__dbname)
            self._conn.row_factory = sqlite3.Row
            if PY_ENV =='dev':
                self._conn.set_trace_callback(print)

            if not self._conn:
                raise Exception("No connection!!")
        except Error as e:
            log.error(e)
            sys.exit()

    def _close(self)->None:
        try:
            self._conn.close()
        except Error as e:
            log.error(e)
            pass

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

if __name__ == "__main__":
    pass
