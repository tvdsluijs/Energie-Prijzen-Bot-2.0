from decimal import Decimal
import os
import logging
from telegram.utils.helpers import escape_markdown

from datetime import datetime, timedelta

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

from functions_sql.prices_sql import PricesSQL

class Prices(PricesSQL):
    def __init__(self,*args, **kwargs) -> None:

        self.morgen = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00']
        self.middag = ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

        self.weekdays = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']
        self.months = ['', 'Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni', 'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December']

        super().__init__(*args, **kwargs)

    def add_prices(self, data:dict = None)->bool:
        try:
            for d in data:
                self._add_price(data=d)
            return True
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_cur_price(self, date:str = None, time:str = None)->str:
        try:
            vandaag_ts = datetime.now()
            if date is None:
                date = vandaag_ts.strftime("%Y-%m-%d")

            if time is None:
                time = vandaag_ts.strftime("%H:00")

            data = self._get_prices(date=date)
            gas = None
            elect = None

            for v in data:
                if v['kind'] == 'e' and v['fromtime'] == time:
                    elect = v
                if v['kind'] == 'g' and v['fromtime'] == time:
                    gas = v

            elect_price = self.dutch_floats(price=elect['price'])
            gas_price= self.dutch_floats(price=gas['price'])

            return f"""
Inkoopprijzen van {elect['fromtime']} tot {self.next_hour(hour=time)}
💡 {elect_price}
🔥 {gas_price}"""

        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def ochtend_prices(self)->dict:
        try:
            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")

            data = self.get_low_high(date=vandaag)

            fromtime_low = data['elect_low'][0]['fromtime']
            int_hour_low = int(fromtime_low[:2])
            price = data['elect_low'][0]['price']
            low_price = self.dutch_floats(price)

            i = 0
            for d in data['elect_low']:
                if i == 0:
                    i += 1
                    continue

                next_low = d['fromtime']
                int_next_low = int(next_low[:2])
                if (int_next_low - int_hour_low) == 1:
                    if Decimal(price) == Decimal(d['price']):
                        int_hour_low = int_next_low
                    else:
                         break
                else:
                    break

            fromtime_high = data['elect_high'][0]['fromtime']
            high_price = self.dutch_floats(data['elect_high'][0]['price'])

            int_hour_low = int(int_hour_low) + 1
            int_hour_high = int(fromtime_high[:2]) + 1
            totime_low = f"{int_hour_low:02d}:00"
            totime_hight = f"{int_hour_high:02d}:00"
            return f"Vandaag is de inkoopprijs van 💡 per kWh het laagst tussen {fromtime_low} en {totime_low} ({low_price}) en het hoogst tussen {totime_hight} en {fromtime_high} ({high_price})"
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_next_hour_price(self, date:str=None, next_hour:str=None, kind:int = 1):
        try:
            data = self._get_next_hour_price(date=date, next_hour=next_hour,kind=kind)
            prijs = data['price']
            msg = f"Om {next_hour} gaat de 💡 prijs naar {self.dutch_floats(prijs)}"
            return {'prijs': prijs, 'msg': msg}
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def vandaag_prices(self)->dict:
        try:
            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")
            data = self._get_prices(date=vandaag)
            return self.totaal_overzicht(data=data, date=vandaag)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def morgen_prices(self, data:dict = None)->str:
        try:
            morgen_ts = datetime.now() + timedelta(days=+1)
            morgen = morgen_ts.strftime("%Y-%m-%d")

            if data is None:
                data = self.morgen_prices_data(date=morgen)

            return self.totaal_overzicht(data=data, date=morgen)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def morgen_prices_data(self, date:str = None)->dict:
        try:
            if date is None:
                morgen_ts = datetime.now() + timedelta(days=+1)
                date = morgen_ts.strftime("%Y-%m-%d")

            return self._get_prices(date=date)
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def totaal_overzicht(self, data:list=None, date:str=None)->str:
        try:
            msg_elect = f"""{self.get_nice_day(date=date)}
Prijzen 💡"""
            msg_gas =  f"Prijzen 🔥"
            gas_voor = ""
            gas_na = ""
            elec = ""
            msg = ""
            electra = {}

            for v in data:
                if v['kind'] == 'e':
                    price = self.dutch_floats(price=v['price'])
                    electra[v['fromtime']] = price
                if v['kind'] == 'g':
                    tijd = int(v['fromtime'][:-3])
                    if tijd <= 5:
                        price = self.dutch_floats(price=v['price'])
                        gas_voor = f"tot 06:00 {price}"
                    else:
                        price = self.dutch_floats(price=v['price'])
                        gas_na = f"na 06:00 {price}"

            for index,item in enumerate(self.morgen):
                elec += f"{self.morgen[index]} {electra[self.morgen[index]]}  {self.middag[index]} {electra[self.middag[index]]}\n"

            msg = f"""{msg_elect}```

{escape_markdown(elec, version=2)}```
{msg_gas}
```
{escape_markdown(gas_voor, version=2)}
{escape_markdown(gas_na, version=2)}```"""
            return msg
        except KeyError as e:
            # Some prices not here, so return
            return False
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def get_low_high(self, date:str = None)->dict:
        try:
            if date is None:
                vandaag_ts = datetime.now()
                date = vandaag_ts.strftime("%Y-%m-%d")

            elect_low = self._get_low_prices(date=date, kind='e')
            elect_high = self._get_high_prices(date=date, kind='e')

            return {'elect_low': elect_low, 'elect_high': elect_high}

        except Exception as e:
            log.error(e, exc_info=True)
            return self.foutmelding

    def get_first_price(self):
        try:
            return self._get_first_price()
        except Exception as e:
            log.error(e, exc_info=True)

    def get_last_price(self):
        try:
            return self._get_last_price()
        except Exception as e:
            log.error(e, exc_info=True)


    def get_nice_day(self, date:str = None) -> str:
            try:
                if date is None:
                    date = self.today

                date = f"{date} 01:01:01"
                dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

                day = dt.strftime("%d")
                weekday = self.weekdays[dt.weekday()]
                month_int = int(dt.strftime("%m"))
                month = self.months[month_int]

                return f"{weekday} {day} {month}"

            except Exception as e:
                log.error(e, exc_info=True)

    @staticmethod
    def dutch_floats(price:float = None,f:str=':.3f')->str:
        return ('€ {'+f+'}').format(price).replace('.',',')

    @staticmethod
    def next_hour(hour:str= None)->str:
        try:
            if hour is None:
                raise Exception('Geen uur mee gegeven')
            int_hour = int(hour[:2]) + 1
            return f"{int_hour:02d}:00"
        except Exception as e:
            log.error(e, exc_info=True)