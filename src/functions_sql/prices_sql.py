import os
import logging
from sqlite3 import Error, OperationalError, IntegrityError
from functions_sql.main_sql import MainSQL

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class PricesSQL(MainSQL):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _add_price(self, data:dict = None)->bool:
        try:
            short_tuple = (data['fromdate'], data['fromtime'], data['kind'], data['price'])
            self._connection()
            sql = """ INSERT OR IGNORE INTO energy (fromdate,fromtime,kind,price)
                    VALUES(?,?,?,?) """
            cur = self._conn.cursor()
            cur.execute(sql, short_tuple)
            self._conn.commit()
            return True
        except KeyError as e:
            log.error(f"KeyError {e}")
            return False
        except OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.no_table(table='energy')
            else:
                log.error(e)
        except IntegrityError as err:
            log.error(e)
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_next_hour_price(self, date:str = None, next_hour:str = None, kind:int = 1)->float:
        try:

            if kind == 1:
                kind = 'e'
            else:
                kind = 'g'

            if date is None or next_hour is None:
                return False

            self._connection()
            cur = self._conn.cursor()
            SQL =  f"""SELECT price
FROM energy
WHERE fromdate = ?
AND fromtime = ?
AND kind = ?"""

            output_obj = cur.execute(SQL, (date, next_hour, kind, ))
            return output_obj.fetchone()

        except IntegrityError:
            return False
        except Exception as e:
            log.error(e)
            return False

    def _get_prices(self, date:str = None, kind:str = None)->dict:
        try:
            self._connection()
            cur = self._conn.cursor()
            if date is None:
                raise Exception('Er is geen datum om prijzen op te halen!')

            if kind is not None:
                SQL = f"""SELECT fromdate, fromtime, price, kind
                      FROM energy
                      WHERE fromdate = ? AND kind = ?"""
                output_obj = cur.execute(SQL, (date, kind, ))
            else:
                SQL =  f"""SELECT fromdate, fromtime, price, kind
                        FROM energy
                        WHERE fromdate = ?;"""
                output_obj = cur.execute(SQL, (date, ))

            results = output_obj.fetchall()
            rs_as_list = []
            for row in results:
                rs_as_list.append( {output_obj.description[i][0]:row[i] for i in range(len(row))} )

            return rs_as_list

        except IntegrityError:
            return False
        except Exception as e:
            log.error(e)
            return False

    def _get_high_prices(self, date:str = None, kind:str = 'e')->dict:
        try:
            self._connection()
            cur = self._conn.cursor()

            SQL =  f"""SELECT fromdate, fromtime, price, kind
FROM energy
WHERE fromdate = ?
AND kind = ?
AND price = ( SELECT max(price) FROM energy
WHERE fromdate = ?
AND kind = ?
Group by fromdate );"""

            output_obj = cur.execute(SQL, (date, kind, date, kind, ))
            results = output_obj.fetchall()

            row_as_dict = []
            for row in results:
                row_as_dict.append( {output_obj.description[i][0]:row[i] for i in range(len(row))} )

            return row_as_dict

        except IntegrityError:
            return 0
        except Exception as e:
            log.error(e)
            return -1

    def _get_low_prices(self, date:str = None, kind:str = 'e')->dict:
        try:
            self._connection()
            cur = self._conn.cursor()

            SQL =  f"""SELECT fromdate, fromtime, price, kind
FROM energy
WHERE fromdate = ?
AND kind = ?
AND price = ( SELECT min(price) FROM energy
WHERE fromdate = ?
AND kind = ?
Group by fromdate );"""

            output_obj = cur.execute(SQL, (date, kind, date, kind, ))
            results = output_obj.fetchall()

            row_as_dict = []
            for row in results:
                row_as_dict.append( {output_obj.description[i][0]:row[i] for i in range(len(row))} )

            return row_as_dict

        except IntegrityError:
            return False
        except Exception as e:
            log.error(e)
            return False

    def _get_first_price(self)->dict:
        try:
            self._connection()
            cur = self._conn.cursor()
            prijzen = {}
            kinds = ['e','g']
            for kind in kinds:
                SQL =  f"""SELECT *
FROM energy
where kind = ?
ORDER BY fromdate ASC, fromtime ASC
LIMIT 1;"""
                output_obj = cur.execute(SQL, (kind, ))
                prijzen[kind] = output_obj.fetchone()

            return prijzen
        except IntegrityError:
            return False
        except Exception as e:
            log.error(e)
            return False


    def _get_last_price(self)->dict:
        try:
            self._connection()
            cur = self._conn.cursor()
            prijzen = {}
            kinds = ['e','g']
            for kind in kinds:
                SQL =  f"""SELECT *
FROM energy
where kind = ?
ORDER BY fromdate DESC, fromtime DESC
LIMIT 1;"""
                output_obj = cur.execute(SQL, (kind, ))
                prijzen[kind] = output_obj.fetchone()

            return prijzen
        except IntegrityError:
            return False
        except Exception as e:
            log.error(e)
            return False
