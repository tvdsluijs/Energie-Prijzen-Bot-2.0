import os,sys
from datetime import datetime, timedelta
from time import time
import telegram
from telegram import ParseMode
from telegram.utils.helpers import escape_markdown

import logging

from functions.api_energyzero import EnergieZero_API
from functions.api_entsoe import Entsoe_API
from functions.api_frankenergie import FrankEnergie_API
from functions.help import Help
from functions.prices import Prices
from functions.systeem import Systeem
from functions.tweet import Tweet
from functions.user import Users

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Dispatcher_Functions(object):
    def __init__(self, *args, **kwargs) -> None:
        try:
            self.config = kwargs['config']

            self.dbname = self.config['db']['name']

            admin_ids = self.config['telegram']['admin_ids'].split(',')
            self.admin_ids = [int(i) for i in admin_ids]

            self.telegram_key = self.config['telegram']['key']
            self.entsoe_key = self.config['entsoe']['key']
            self.path = self.config['other']['path']
            self.startTime = self.config['other']['startTime']

            self.date_hours = []
            super().__init__()
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.critical(e)

    def auto_bot(self, context: telegram.ext.CallbackContext)->None:
        #deze functie handelt automatische meldingen af en haalt de energie prijzen op
        try:
            now = datetime.now()
            cur_hour = int(now.strftime("%H"))

            #If it returns False, it alrady ran this hour
            if not self.check_run_now():
                return

            self.process_new_prices()
            self.ochtend_melding(context=context, hour=cur_hour)
            self.middag_melding(context=context, hour=cur_hour)

            # self.onder_bedrag_melding(context=context)
            # self.boven_bedrag_melding(context=context)

        except Exception as e:
            log.error(e, exc_info=True)

    def start_me_up(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            H = Help()
            msg = H.start_text(update=update)
            del H
            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_current(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            P = Prices(dbname=self.dbname)
            if not (msg := P.get_cur_price()):
                msg = "Sorry er ging iets fout"
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_today(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            P = Prices(dbname=self.dbname)
            if not (msg := P.vandaag_prices()):
                msg = "Sorry er ging iets fout"
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_tomorrow(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            P = Prices(dbname=self.dbname)
            if not (msg := P.morgen_prices()):
                msg = "Er zijn op dit moment nog geen prijzen voor morgen"
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def show_highprices(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            return
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)
        pass

    def show_lowprices(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            return
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)
        pass

    def help(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            H = Help()
            msg = H.help_text(update=update)
            del H
            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def donate(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.donatie_help()
                else:
                    raise IndexError
            except IndexError:
                msg = "https://donorbox.org/tvdsluijs-github"

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def systeminfo(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.systeem_help()
                else:
                    raise IndexError
            except IndexError:
                versie_path = os.path.join(self.path, "VERSION.TXT")
                version = open(versie_path, "r").read().replace('\n','')
                seconds = int(time()) - int(self.startTime)

                U = Users(dbname=self.dbname)
                print(U.get_users())
                users = len(U.get_users())
                del U

                S = Systeem()

                msg = S.systeminfo_msg(version=version, users=users, seconds=seconds, dbname=self.dbname)
                del S

            context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
            # context.bot.send_message(chat_id=update.message.chat_id, text=escape_markdown(text=msg, version=2), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def aanmelden(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.aanmelden_help()
                else:
                    raise IndexError
            except IndexError:

                U = Users(dbname=self.dbname)
                user = U.get_user(user_id=update.message.chat_id)
                if user and user['user_id']:
                    msg = "U staat al in het systeem!"
                else:
                    msg = U.save_user(user_id=update.message.chat_id, msg=True)

                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def verwijderme(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.afmelden_help()
                else:
                    raise IndexError
            except IndexError:
                U = Users(dbname=self.dbname)
                user = U.get_user(user_id=update.message.chat_id)
                if not user or user['user_id'] < 0:
                    msg = "U staat niet in het systeem!"
                else:
                    msg = U.del_user(user_id=update.message.chat_id, msg=True)

                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.error(e, exc_info=True)

    def instellingen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.get_instellingen_help()
            except IndexError:
                U = Users(dbname=self.dbname)
                user = U.get_user(user_id=update.message.chat_id)
                msg = U.get_instellingen(user=user)

                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def ochtend_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.ochtend_instellen_help()
            except IndexError:
                U = Users(dbname=self.dbname)
                msg = U.set_ochtend(context=context, user_id=update.message.chat_id)
                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def ld_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.ld_instellen_help()
            except IndexError:
                U = Users(dbname=self.dbname)
                msg = U.set_middag(context=context, user_id=update.message.chat_id)
                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)


    def hd_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.hd_instellen_help()
            except IndexError:
                U = Users(dbname=self.dbname)
                msg = U.set_middag(context=context, user_id=update.message.chat_id)
                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)


    def middag_instellen(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        try:
            try:
                if context.args[0] == 'help':
                    H = Help()
                    msg = H.middag_instellen_help()
            except IndexError:
                U = Users(dbname=self.dbname)
                msg = U.set_middag(context=context, user_id=update.message.chat_id)
                del U

            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
        except Exception as e:
            log.error(e, exc_info=True)

    def onder_bedrag_melding(self, context: telegram.ext.CallbackContext)->None:
        try:

            next_hour_ts = datetime.now()+ timedelta(hours=+1)
            next_hour = next_hour_ts.strftime("%H:00")
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")

            P = Prices(dbname=self.dbname)
            if (prijs_message := P.get_next_hour_price(date=date, next_hour=next_hour, kind=1)):
                U = Users(dbname=self.dbname)
                ids = U.get_lower_price_users(price=prijs_message['prijs'])
                if ids:
                    for id in ids:
                        if id == 0:
                            continue
                        context.bot.send_message(chat_id=id, text=prijs_message['msg'], parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def boven_bedrag_melding(self, context: telegram.ext.CallbackContext)->None:
        try:
            next_hour_ts = datetime.now()+ timedelta(hours=+1)
            next_hour = next_hour_ts.strftime("%H:00")
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")

            P = Prices(dbname=self.dbname)
            if (prijs_message := P.get_next_hour_price(date=date, next_hour=next_hour, kind=1)):
                U = Users(dbname=self.dbname)
                ids = U.get_higher_price_users(price=prijs_message['prijs'])
                if ids:
                    for id in ids:
                        if id == 0:
                            continue
                        context.bot.send_message(chat_id=id, text=prijs_message['msg'], parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            log.error(e, exc_info=True)

    def middag_melding(self, context: telegram.ext.CallbackContext, hour:int=15)->None:
        try:
            morgen_ts = datetime.now() + timedelta(days=+1)
            morgen = morgen_ts.strftime("%Y-%m-%d")

            P = Prices(dbname=self.dbname)
            data = P.morgen_prices_data(date=morgen)
            el_prices = 0
            try:
                for d in data:
                    if d['kind'== 'e']:
                        el_prices = 1
                        break

                # No electric prices yet, so return
                if el_prices == 0:
                    return False

            except KeyError:
                return False

            U = Users(dbname=self.dbname)
            ids = U.get_middag_users(hour=hour)
            ids.append(0)
            del U
            if ids:
                #get morgen message
                if not (msg := P.morgen_prices(data=data)):
                    return False
                for id in ids:
                    if id == 0:
                        continue
                    context.bot.send_message(chat_id=id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)

            del P
        except Exception as e:
            log.error(e, exc_info=True)

    def ochtend_melding(self, context: telegram.ext.CallbackContext, hour:int=8)->None:
        try:
            U = Users(dbname=self.dbname)
            ids = U.get_ochtend_users(hour=hour)
            ids.append(0)
            del U
            #get ochtend message
            P = Prices(dbname=self.dbname)
            if not (msg := P.ochtend_prices()):
                raise Exception('Geen ochtend prijzen op kunnen halen')
            del P

            if hour == 8:
                tweet = msg + " Meer zien? Volg de telegram bot! https://t.me/EnergiePrijzen_bot"
                T = Tweet(config=self.config)
                T.tweettie(msg=tweet)
                del T

            if ids:
                for id in ids:
                    if id == 0:
                        continue
                    telebot = msg + " Meer prijzen zien? /vandaag"
                    context.bot.send_message(chat_id=id, text=telebot)

        except Exception as e:
            log.error(e, exc_info=True)

    def process_new_prices(self)->bool:
        try:
            P = Prices(dbname=self.dbname)

            #stroom = 1, gas = 2
            # Gas ophalen bij ernergyzero
            EZ = EnergieZero_API()
            if (data := EZ.get_data(kind=2)):
                del EZ
                pass
            else:
                FE = FrankEnergie_API()
                if (data := FE.get_data(kind=2)): #gas ophalen bij Frank
                    del FE
                    pass
            P.add_prices(data=data) #opslaan gasprijzen!

            # Electra ophalen bij entsoe
            EN = Entsoe_API()
            if (data := EN.get_data(entsoe_key=self.entsoe_key)):
                del EN
                pass
            #wanneer er geen data is dan bij frankenergie ophalen.
            else:
                FE = FrankEnergie_API()
                if (data := FE.get_data(kind=1)):
                    del FE
                    pass
                else:
                    #wanneer er geen data is dan bij energyzero ophalen.
                    EZ = EnergieZero_API()
                    if (data := EZ.get_data(kind=1)):
                        del EZ
                        pass

            P.add_prices(data=data) #opslaan electra prijzen

        except Exception as e:
            log.error(e, exc_info=True)

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
