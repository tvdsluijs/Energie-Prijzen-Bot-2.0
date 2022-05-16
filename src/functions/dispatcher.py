import os
# import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
from functions.dispatcher_functions import Dispatcher_Functions
from telegram.ext.filters import Filters

import logging

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Dispatcher(Dispatcher_Functions):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def start_dispatch(self)->None:
        try:
            u = Updater(self.telegram_key, use_context=True)
            j = u.job_queue

            # run every minute
            job_minute = j.run_repeating(self.auto_bot, interval=60, first=1) #iedere minuut

            start_handler = CommandHandler('start', self.start_me_up)
            u.dispatcher.add_handler(start_handler)

            aanmelden_handler = CommandHandler(['a','aanmelden'], self.aanmelden)
            u.dispatcher.add_handler(aanmelden_handler)

            instellingen_handler = CommandHandler(['i','instellingen'], self.instellingen)
            u.dispatcher.add_handler(instellingen_handler)

            afmelden_handler = CommandHandler(['v','afmelden','verwijderme'], self.verwijderme)
            u.dispatcher.add_handler(afmelden_handler)

            ochtend_handler = CommandHandler(['o','ochtend'], self.ochtend_instellen)
            u.dispatcher.add_handler(ochtend_handler)

            middag_handler = CommandHandler(['m','middag'], self.middag_instellen)
            u.dispatcher.add_handler(middag_handler)

            ldinstellen_handler = CommandHandler(['ld','lagerdan'], self.ld_instellen)
            u.dispatcher.add_handler(ldinstellen_handler)

            hsinstellen_handler = CommandHandler(['hd','hogerdan'], self.hd_instellen)
            u.dispatcher.add_handler(hsinstellen_handler)

            current_handler = CommandHandler('nu', self.show_current)
            u.dispatcher.add_handler(current_handler)

            today_handler = CommandHandler('vandaag', self.show_today)
            u.dispatcher.add_handler(today_handler)

            tomorrow_handler = CommandHandler('morgen', self.show_tomorrow)
            u.dispatcher.add_handler(tomorrow_handler)

            # highprice_handler = CommandHandler('hoog', self.show_highprices)
            # u.dispatcher.add_handler(highprice_handler)

            # lowprice_handler = CommandHandler('laag', self.show_lowprices)
            # u.dispatcher.add_handler(lowprice_handler)

            help_handler = CommandHandler(['h', 'help', 'hulp'], self.help)
            u.dispatcher.add_handler(help_handler)

            donate_handler = CommandHandler(['d','doneer', 'donatie', 'doneren'], self.donate)
            u.dispatcher.add_handler(donate_handler)

            system_handler = CommandHandler(['s', 'system', 'systeem'], self.systeminfo)
            u.dispatcher.add_handler(system_handler)

            #anything else
            unknown_handler = MessageHandler(Filters.command, self.help)
            u.dispatcher.add_handler(unknown_handler)

            blahblah_handler = MessageHandler(Filters.text, self.help)
            u.dispatcher.add_handler(blahblah_handler)

            # Start the Bot
            u.start_polling()
            u.idle()
        except Exception as e:
            log.error(e)
            pass
