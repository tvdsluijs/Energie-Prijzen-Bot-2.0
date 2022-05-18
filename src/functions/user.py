import os
import logging

import telegram

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

from functions_sql.users_sql import UsersSQL

class Users(UsersSQL):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def save_user(self, user_id:int = None, msg:bool = False)->bool:
        try:
            if user_id is None:
                return False
            if self._add_user(user_id=user_id):
                if msg:
                    return """U bent toegevoegd aan het systeem!
U krijgt rond 8 uur en rond 16 uur een autmatisch prijzen bericht.
U krijg ook bericht wanneer de prijzen onder de 0.001 zakt."""
                else:
                    return True
        except Exception as e:
            log.error(e, exc_info=True)
            if msg:
                return "Er is iets fout gegaan bij het opslaan van de gebruiker"
            else:
                return False

    def get_user(self, user_id:int = None)->bool:
        try:
            if user_id is None:
                return False
            return self._get_user(user_id=user_id)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_users(self)->list:
        try:
            return self._get_users()
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def del_user(self, user_id:int = None, msg:bool = False)->str:
        try:
            if user_id is None:
                return False
            if self._remove_user(user_id=user_id):
                if msg:
                    return """U bent verwijderd uit het systeem!
U ontvangt geen berichten meer. U kunt nog wel gebruik maken van deze Bot.
"""
                else:
                    return True
        except Exception as e:
            log.error(e, exc_info=True)
            if msg:
                return "Er is iets fout gegaan bij het verwijderen"
            else:
                return False

    def get_ochtend_users(self, hour:int=8)->list:
        try:
            return self._get_ochtend_users(hour=hour)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_middag_users(self, hour:int=15)->list:
        try:
            return self._get_middag_users(hour=hour)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_lower_price_users(self, price:float=0.001)->list:
        try:
            return self._get_lower_price_users(price=price)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_higher_price_users(self, price:float=0.200)->list:
        try:
            return self._get_higher_price_users(price=price)
        except Exception as e:
            log.error(e, exc_info=True)
            return False


    def get_instellingen(self, user:dict = None)->str:
        try:
            if user is None or user['user_id'] < 0:
                raise KeyError
            else:
                msg = f"""Uw chat id is {user['user_id']}
U ontvangt de volgende berichten:
"""
                if user['ochtend'] is not None:
                    msg += f"""
Ochtend update om ±{user['ochtend']} uur"""
                else:
                    msg += """
Geen ochtend update"""
                if user['middag'] is not None:
                    msg += f"""
Middag bericht om ±{user['middag']} uur"""
                else:
                    msg += """
Geen middag update"""
                if user['melding_lager_dan'] is not None:
                    msg += f"""
Bedrag lager dan {user['melding_lager_dan']}"""
                else:
                    msg += """
Geen bedrag lager dan update"""
                if user['melding_hoger_dan'] is not None:
                    msg += f"""
Bedrag hoger dan {user['melding_hoger_dan']}"""
                else:
                    msg += """
Geen bedrag hoger dan update"""

            msg += """

Hulp? /instellingen help
"""
            return msg
        except KeyError:
            return """
U staat niet in het systeem!

Aanmelden voor automatische updates?
/aanmelden
of
/a"""
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def set_ochtend(self, context: telegram.ext.CallbackContext, user_id:int = None)->bool:
        aan_uit = None
        try:
            try:
                if context.args[0] == 'aan' :
                    aan_uit = 1
                elif context.args[0] == 'uit':
                    aan_uit = 0
                else:
                    raise IndexError
            except IndexError:
                return """Ik begrijp je niet
Wil je iets doen zoals:
/ochtend aan 8
/ochtend uit
"""
            except Exception as e:
                log.error(e, exc_info=True)

            try:
                if aan_uit == 1:
                    data = self._set_ochtend_user(user_id=user_id, hour=context.args[1])
                elif aan_uit == 0:
                    data = self._set_ochtend_user(user_id=user_id, hour=None)
            except IndexError:
                return """U bent een tijd vergeten
/ochtend aan 8
/ochtend aan 9
"""
            if data:
                return "Uw ochtend melding is opgeslagen"
            else:
                return "Er ging iets fout"

        except Exception as e:
            log.error(e, exc_info=True)

    def set_middag(self, context: telegram.ext.CallbackContext, user_id:int = None)->bool:
        aan_uit = None
        try:
            try:
                if context.args[0] == 'aan' :
                    aan_uit = 1
                elif context.args[0] == 'uit':
                    aan_uit = 0
                else:
                    raise IndexError
            except IndexError:
                return """Ik begrijp je niet
Wil je iets doen zoals:
/middag aan 16
/middag uit
"""
            except Exception as e:
                log.error(e, exc_info=True)

            try:
                if aan_uit == 1:
                    data = self._set_middag_user(user_id=user_id, hour=context.args[1])
                elif aan_uit == 0:
                    data = self._set_middag_user(user_id=user_id, hour=None)
            except IndexError:
                return """U bent een tijd vergeten
/middag aan 15
/middag aan 14
"""
            if data:
                return "Uw middag melding is opgeslagen"
            else:
                return "Er ging iets fout"

        except Exception as e:
            log.error(e, exc_info=True)
