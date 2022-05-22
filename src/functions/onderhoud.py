import os
import logging
import telegram

from functions.user import Users

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Onderhoud:
    def __init__(self) -> None:
        pass

    def start(self, context: telegram.ext.CallbackContext)->str:
        """Een functie waarmee je onderhoud aan of uit kan zetten"""
        """en een melding geeft naar alle gebruikers"""
        try:

            try:
                aan_uit = context.args[0]
            except IndexError:
                return False

            match aan_uit:
                case 'aan':
                    return self._aan()
                case 'uit':
                    return self._uit()

        except Exception as e:
            log.error(e)
            return False

    def _aan(self)->str:
        try:
            return "We gaan even in ouderhoud voor updates! We zijn zo weer terug!"
        except Exception as e:
            log.error(e)
            return False

    def _uit(self)->str:
        try:
            return "Het onderhoud is gedaan. We zijn weer terug!"
        except Exception as e:
            log.error(e)
            return False


    def _kweetnie(self)->str:
        try:
            return """
Ik begrijp je niet, het commando is
/onderhoud aan
/onderhoud uit"""
        except Exception as e:
            log.error(e)
            return False