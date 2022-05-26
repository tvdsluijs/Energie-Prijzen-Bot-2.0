import os
from datetime import datetime, timedelta
import sys
from time import time
import telegram
from telegram import ParseMode
from telegram.utils.helpers import escape_markdown

import logging

from functions.api_energyzero import EnergieZero_API
from functions.api_entsoe import Entsoe_API
from functions.api_frankenergie import FrankEnergie_API
from functions.help import Help
from functions.onderhoud import Onderhoud
from functions.prices import Prices
from functions.stuur_bericht import StuurBericht
from functions.systeem import Systeem
from functions.tweet import Tweet
from functions.user import Users

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class UnKnownException(Exception):
    pass

class Dispatcher_Functions(object):
    def __init__(self, *args, **kwargs) -> None:
        try:
            self.config = kwargs['config']

            self.dbname = self.config['db']['name']

            admin_ids = self.config['telegram']['admin_ids'].split(',')
            self.admin_ids = [int(i) for i in admin_ids]

            self.telegram_key = self.get_telegram_key()
            self.entsoe_key = self.config['entsoe']['key']
            self.path = self.config['other']['path']
            self.startTime = self.config['other']['startTime']

            self.twitter_ochtend_hour = 8
            self.twitter_middag_hour = 15
            self.kweetniet = "Sorry dit commando begrijp ik niet."
            self.hashtags = "\n #energie #energieprijzen #energietarieven #gasprijs"

            self.date_hours = []
            super().__init__()
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.critical(e, exc_info=True)

    def get_telegram_key(self)->str:
        try:
            match PY_ENV:
                case 'dev':
                    return self.config['telegram']['dev_key']
                case 'acc':
                    return self.config['telegram']['acc_key']
                case 'prod':
                    return self.config['telegram']['prod_key']
                case _:
                    return self.config['telegram']['dev_key']
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.critical(e, exc_info=True)

    def auto_bot(self, context: telegram.ext.CallbackContext)->None:
        #deze functie handelt automatische meldingen af en haalt de energie prijzen op
        try:
            now = datetime.now()
            cur_hour = int(now.strftime("%H"))

            #If it returns False, it alrady ran this hour
            if not self.check_run_now():
                return

            self.process_new_prices()
            self.tweet_current()
            self.ochtend_melding(context=context, hour=cur_hour)
            self.middag_melding(context=context, hour=cur_hour)
            self.onder_bedrag_melding(context=context)

            # self.boven_bedrag_melding(context=context)

        except Exception as e:
            log.error(e, exc_info=True)

    def start_me_up(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = Help.start_text(update=update)
            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def bericht(self, update: telegram.Update, context: telegram.ext.CallbackContext)->None:
        try:
            if int(update.message.chat_id) not in self.admin_ids:
                msg = "Sorry ik weet niet wat u bedoelt"
                context.bot.send_message(chat_id=update.message.chat_id, text=msg)
                return

            try:
                msg  = ' '.join(context.args)
            except IndexError:
                return False
            except Exception:
                return False

            if msg is not None and msg != "":
                StuurBericht(dbname=self.dbname)._alle_gebuikers(context=context,msg=msg)

        except Exception as e:
            log.error(e, exc_info=True)

    def onderhoud(self, update: telegram.Update, context: telegram.ext.CallbackContext)->None:
        try:
            if int(update.message.chat_id) not in self.admin_ids:
                raise UnKnownException(self.kweetniet)

            if (msg := Onderhoud().start(context=context)):
                StuurBericht(dbname=self.dbname)._alle_gebuikers(context=context,msg=msg)
            else:
                raise UnKnownException(Onderhoud()._kweetnie)

        except UnKnownException as msg:
            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_current(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            if not (msg := Prices(dbname=self.dbname).get_cur_price()):
                msg = "Sorry er ging iets fout"
            context.bot.send_message(chat_id=update.message.chat_id, text=escape_markdown(msg, version=2), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_today(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            if not (msg := Prices(dbname=self.dbname).vandaag_prices()):
                msg = "Sorry er ging iets fout"
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_tomorrow(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            if not (msg := Prices(dbname=self.dbname).morgen_prices()):
                msg = "Er zijn op dit moment nog geen prijzen voor morgen"
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_highprices(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """Deze functie doet nog ff niks"""
        try:
            return
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)
        pass

    def show_lowprices(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """Deze functie doet nog ff niks"""
        try:
            return
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)
        pass

    def help(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = Help.help_text(update=update)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=msg, parse_mode=ParseMode.MARKDOWN_V2,
                                     disable_web_page_preview=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def donate(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            try:
                if context.args[0] == 'help':
                    msg = Help.donatie_help()
                else:
                    raise IndexError
            except IndexError:
                msg = "https://donorbox.org/tvdsluijs-github"

            context.bot.send_message(chat_id=update.message.chat_id, text=msg,
                                     disable_web_page_preview=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def systeminfo(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = escape_markdown(Help.systeem_help(), version=2)
            except IndexError:
                pass

            if msg is None or msg == "":
                versie_path = os.path.join(self.path, "VERSION.TXT")
                version = open(versie_path, "r").read().replace('\n','')
                seconds = int(time()) - int(self.startTime)
                users = len(Users(dbname=self.dbname).get_users())
                msg = Systeem().systeminfo_msg(version=version, users=users, seconds=seconds, dbname=self.dbname)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2,
                                     disable_web_page_preview=True )

        except Exception as e:
            log.error(e, exc_info=True)

    def aanmelden(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    msg = Help.aanmelden_help()
                else:
                    raise IndexError
            except IndexError:
                user = Users(dbname=self.dbname).get_user(user_id=update.message.chat_id)
                if user and user['user_id']:
                    msg = "U staat al in het systeem!"
                else:
                    msg = Users(dbname=self.dbname).save_user(user_id=update.message.chat_id, msg=True)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def verwijderme(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.afmelden_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                user = Users(dbname=self.dbname).get_user(user_id=update.message.chat_id)
                if not user or user['user_id'] < 0:
                    msg = "U staat niet in het systeem!"
                else:
                    msg = Users(dbname=self.dbname).del_user(user_id=update.message.chat_id, msg=True)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def instellingen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.get_instellingen_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                user = Users(dbname=self.dbname).get_user(user_id=update.message.chat_id)
                if not (msg := Users(dbname=self.dbname).get_instellingen(user=user)):
                    msg = "Sorry er ging iets fout!"

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def ochtend_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.ochtend_instellen_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                msg = Users(dbname=self.dbname).set_ochtend(context=context, user_id=update.message.chat_id)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def ld_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        """Lager Dan prijs instellen"""
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.ld_instellen_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                msg = Users(dbname=self.dbname).set_lagerdan(context=context, user_id=update.message.chat_id)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def hd_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        """Hoger Dan prijs instellen"""
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.hd_instellen_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                msg = Users(dbname=self.dbname).set_hogerdan(context=context, user_id=update.message.chat_id)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def middag_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            msg = None
            try:
                if context.args[0] == 'help':
                    msg = Help.middag_instellen_help()
            except IndexError:
                pass

            if msg is None or msg == "":
                msg = Users(dbname=self.dbname).set_middag(context=context, user_id=update.message.chat_id)

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def onder_bedrag_melding(self, context: telegram.ext.CallbackContext)->None:
        try:
            next_hour_ts = datetime.now()+ timedelta(hours=+1)
            next_hour = next_hour_ts.strftime("%H:00")
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")

            if (prijs_message := Prices(dbname=self.dbname).get_next_hour_price(date=date, next_hour=next_hour, kind=1)):
                if (ids := Users(dbname=self.dbname).get_lower_price_users(price=prijs_message['prijs'])):
                    msg = escape_markdown(prijs_message['msg'], version=2)
                    StuurBericht(dbname=self.dbname)._bepaalde_gebruikers_md(context=context, msg=msg, ids=ids)
        except Exception as e:
            log.error(e, exc_info=True)

    def boven_bedrag_melding(self, context: telegram.ext.CallbackContext)->None:
        try:
            next_hour_ts = datetime.now()+ timedelta(hours=+1)
            next_hour = next_hour_ts.strftime("%H:00")
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")

            if (prijs_message := Prices(dbname=self.dbname).get_next_hour_price(date=date, next_hour=next_hour, kind=1)):
                if (ids := Users(dbname=self.dbname).get_higher_price_users(price=prijs_message['prijs'])):
                    msg = escape_markdown(prijs_message['msg'], version=2)
                    StuurBericht(dbname=self.dbname)._bepaalde_gebruikers_md(context=context, msg=msg, ids=ids)

        except Exception as e:
            log.error(e, exc_info=True)

    def middag_melding(self, context: telegram.ext.CallbackContext, hour:int=15)->None:
        try:
            morgen_ts = datetime.now() + timedelta(days=+1)
            morgen = morgen_ts.strftime("%Y-%m-%d")

            data = Prices(dbname=self.dbname).morgen_prices_data(date=morgen)
            el_prices = 0
            try:
                for d in data:
                    if d['kind'] == 'e':
                        el_prices = 1
                        break

                # No electric prices yet, so return
                if el_prices == 0:
                    raise KeyError

            except KeyError as e:
                return False

            #get morgen message
            if not (msg := Prices(dbname=self.dbname).morgen_prices(data=data)):
                return False
            if (ids := Users(dbname=self.dbname).get_middag_users(hour=hour)):
                StuurBericht(dbname=self.dbname)._bepaalde_gebruikers_md(context=context, msg=msg, ids=ids)

            # Lengte van bericht is 416 dus veel te lang om op twitter te laten zien
            # Dus laten we het per uur zien! Zie functie tweet_current
            # if hour == self.twitter_middag_hour:
            #     T = Tweet(config=self.config)
            #     T.tweettie(msg=msg)
            #     del T

        except Exception as e:
            log.error(e, exc_info=True)

    def tweet_current(self)->None:
        """Functie om huidige prijzen naar twitter te sturen"""
        try:
            if not (msg := Prices(dbname=self.dbname).get_cur_price()):
                return False

            msg = msg + " " + self.hashtags
            Tweet(config=self.config).tweettie(msg=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def ochtend_melding(self, context: telegram.ext.CallbackContext, hour:int=8)->None:
        try:
            #get ochtend message
            if not (msg := Prices(dbname=self.dbname).ochtend_prices()):
                raise Exception('Geen ochtend prijzen op kunnen halen')

            if hour == self.twitter_ochtend_hour:
                tweet = msg + " Meer zien? Volg de telegram bot! https://t.me/EnergiePrijzen_bot " + self.hashtags
                Tweet(config=self.config).tweettie(msg=tweet)

            if (ids := Users(dbname=self.dbname).get_ochtend_users(hour=hour)):
                msg = msg + " Meer prijzen zien? /vandaag"
                StuurBericht(dbname=self.dbname)._bepaalde_gebuikers(context=context, msg=msg, ids=ids)
        except Exception as e:
            log.error(e, exc_info=True)

    def process_new_prices(self)->bool:
        try:
            #stroom = 1, gas = 2
            self.process_gas()

            self.process_electra()

        except Exception as e:
            log.error(e, exc_info=True)

    def process_gas(self)->bool:
        try:
            #stroom = 1, gas = 2
            # Gas ophalen bij ernergyzero
            if (data := EnergieZero_API().get_data(kind=2)):
                pass
            elif (data := FrankEnergie_API().get_data(kind=2)): #gas ophalen bij Frank
                pass
            else:
                raise Exception('Geen Gasprijzen?')
            #opslaan gasprijzen!
            if not Prices(dbname=self.dbname).add_prices(data=data):
                raise Exception('Gas opslaan fout!')

            return True
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def process_electra(self)->bool:
        try:
            #stroom = 1, gas = 2
            # Electra ophalen bij entsoe
            if (data := Entsoe_API().get_data(entsoe_key=self.entsoe_key)):
                pass
            #wanneer er geen data is dan bij frankenergie ophalen.
            elif (data := FrankEnergie_API().get_data(kind=1)):
                pass
            elif (data := EnergieZero_API().get_data(kind=1)):
                pass
            else:
                raise Exception('Geen electra prijzen?')
             #opslaan electra prijzen
            if not Prices(dbname=self.dbname).add_prices(data=data):
                raise Exception('Electra opslaan fout!')

            return True
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def check_run_now(self)->bool:
        try:
            now = datetime.now()
            date_hour = now.strftime("%Y-%m-%d %H:00")

            # Check if current hour in , if so do not run!
            if date_hour in self.date_hours:
                return False #don't run!

            # hour not in list so do somehtings
            self.date_hours.append(date_hour) # add hour to list
            self.date_hours = self.date_hours[-5:] # remove last hour
            return True # RUN RUN RUN
        except Exception as e:
            log.error(e, exc_info=True)
