import sys
import os
import logging

from functions_sql.main_sql import MainSQL

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class TablesSQL(MainSQL):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def no_table(self, table:str = None)->bool:
        try:
            sql = ""
            if table == 'user':
                sql = """ CREATE TABLE IF NOT EXISTS users (
                            user_id           INTEGER     PRIMARY KEY,
                            datetime          INTEGER,
                            ochtend           INTEGER,
                            opslag            DOUBLE,
                            melding_lager_dan DECIMAL DEFAULT (0.001),
                            melding_hoger_dan DECIMAL
                                        ); """

            if table == "energy":
                sql = """ CREATE TABLE IF NOT EXISTS energy(
                        fromdate VARCHAR(10) NOT NULL,
                        fromtime VARCHAR(5) NOT NULL,
                        kind VARCHAR(10) NOT NULL,
                        price DOUBLE NOT NULL,
                        PRIMARY KEY(fromdate,fromtime,kind)
                        ); """
            if sql != "":
                self.create_table(create_table_sql=sql)
                return True
            else:
                raise Exception("There is no SQL to run!!")
        except Exception as e:
            log.error(e)
            return False

    def create_table(self, create_table_sql:str=None)->None:
        try:
            if not create_table_sql:
                raise Exception('No create table SQL')

            self._connection()
            cur = self._conn.cursor()
            cur.execute(create_table_sql)
            self._conn.commit()
            return True
        except Exception as e:
            log.error(f'Cannot create table: {e}, {create_table_sql}')
            sys.exit(f'Cannot create table: {e}, {create_table_sql}')