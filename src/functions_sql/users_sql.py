import os
import logging
from time import time
from sqlite3 import Error, OperationalError, IntegrityError
from functions_sql.main_sql import MainSQL

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class UsersSQL(MainSQL):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _add_user(self, user_id:int = None)->int:
        """user toevoegen met user_id als int en time als int"""
        short_tuple = (user_id, int(time()))
        try:
            self._connection()
            sql = """INSERT INTO users (user_id, datetime)
                    VALUES(?,?)"""
            cur = self._conn.cursor()
            cur.execute(sql, short_tuple)
            self._conn.commit()
            return True
        except OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.no_table(table='user')
            else:
                log.debug(e)
            return False
        except IntegrityError as e:
            log.error(e)
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_user(self, user_id:int = None)->dict:
        """user ophalen
        user_id, datetime, kaal_opslag_allin, ochtend, middag, opslag,
        melding_lager_dan, melding_hoger_dan """
        try:
            self._connection()
            cur = self._conn.cursor()
            return cur.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        except Error as e:
            log.error(e)
            return False

    def _get_users(self)->list:
        try:
            self._connection()
            cur = self._conn.cursor()
            cur.execute("SELECT user_id FROM users")
            return [list[0] for list in cur.fetchall()]
        except Error as e:
            log.error(e)
            return False

    def _remove_user(self, user_id:int = None)->bool:
        """user verwijderen via user_id int"""
        try:
            self._connection()
            cur = self._conn.cursor()
            cur.execute(f"DELETE FROM users WHERE user_id=?", (user_id,))
            self._conn.commit()
            return True
        except IntegrityError as e:
            log.error(e)
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_ochtend_users(self, hour:int = None)->list:
        try:
            if hour is None:
                return False

            self._connection()
            cur = self._conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE ochtend = ?", (hour, ))
            return [list[0] for list in cur.fetchall()]
        except IntegrityError as err:
            return False
        except Error as e:
            log.error(e)
            return False

    def _set_ochtend_user(self, user_id:int = None, hour:int = 8)->bool:
        try:
            if user_id is None:
                return False

            user = self._get_user(user_id=user_id)
            if not user:
                self._add_user(user_id=user_id)

            self._connection()
            sql = """Update users
set ochtend = ?
WHERE user_id = ?"""
            cur = self._conn.cursor()
            cur.execute(sql,(hour, user_id,))
            self._conn.commit()
            return True
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e, exc_info=True)
            return False

    def _set_middag_user(self, user_id:int = None, hour:int = 15)->list:
        try:
            if user_id is None:
                return False

            user = self._get_user(user_id=user_id)
            if not user:
                self._add_user(user_id=user_id)

            self._connection()
            sql = """Update users
set middag = ?
WHERE user_id = ?"""
            cur = self._conn.cursor()
            cur.execute(sql,(hour, user_id,))
            self._conn.commit()
            return True
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_middag_users(self, hour:int = None)->list:
        try:
            if hour is None:
                return True

            self._connection()
            cur = self._conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE middag = ?", (hour, ))
            return [list[0] for list in cur.fetchall()]
        except IntegrityError as err:
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_lower_price_users(self, price:float = 0.001)->list:
        try:
            self._connection()
            cur = self._conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE melding_lager_dan > ?", (price, ))
            return [list[0] for list in cur.fetchall()]
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e)
            return False

    def _set_lower_price_user(self, user_id:int = None, price:float = -0.10)->bool:
        try:
            if user_id is None:
                return False

            user = self._get_user(user_id=user_id)
            if not user:
                self._add_user(user_id=user_id)

            self._connection()
            sql = """Update users
set melding_lager_dan = ?
WHERE user_id = ?"""
            cur = self._conn.cursor()
            cur.execute(sql,(price, user_id,))
            self._conn.commit()
            return True
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e)
            return False

    def _get_higher_price_users(self, price:float = 0.001)->list:
        try:
            self._connection()
            cur = self._conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE melding_hoger_dan < ?", (price, ))
            return [list[0] for list in cur.fetchall()]
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e)
            return False

    def _set_higher_price_user(self, user_id:int = None, price:float = None)->bool:
        try:
            if user_id is None:
                return False

            user = self._get_user(user_id=user_id)
            if not user:
                self._add_user(user_id=user_id)

            self._connection()
            sql = """Update users
set melding_hoger_dan = ?
WHERE user_id = ?"""
            cur = self._conn.cursor()
            cur.execute(sql,(price, user_id,))
            self._conn.commit()
            return True
        except IntegrityError as e:
            log.error(e, exc_info=True)
            return False
        except Error as e:
            log.error(e)
            return False
