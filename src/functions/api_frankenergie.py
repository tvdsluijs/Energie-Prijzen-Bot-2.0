import os
from datetime import datetime, timedelta

from pytz import utc
import requests

import functions.api_general

import logging

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class FrankEnergie_API:
    def __init__(self) -> None:
        pass

    def get_data(self, startdate:str = "", enddate:str = "", kind:int = 1)->dict:
        try:
            api_data = self.__get_api_data(startdate=startdate, enddate=enddate, kind=kind)
            if (data := self.__process_api_data(data=api_data, kind=kind, UTC=True)):
                return data

            raise KeyError('No Data?')
        except KeyError as e:
            log.warning(f"We did not get data from FrankEnergie api : {e}")
            return False
        except Exception as e:
            log.error(e)
            return False

    def __get_api_data(self, startdate:str = "", enddate:str = "")->dict:
        try:
            if startdate == "":
                yesterday_ts = datetime.now() + timedelta(days=-1)
                startdate = yesterday_ts.strftime("%Y-%m-%d")
            if enddate == "":
                tomorrow_ts = datetime.now() + timedelta(days=+1)
                enddate = tomorrow_ts.strftime("%Y-%m-%d")

            headers = { "content-type":"application/json" }

            query = f"""query MarketPrices {{
                marketPricesElectricity(startDate: "{startdate}", endDate: "{enddate}") {{
                till
                from
                marketPrice
                priceIncludingMarkup
                }}
                marketPricesGas(startDate: "{startdate}", endDate: "{enddate}") {{
                from
                till
                marketPrice
                priceIncludingMarkup
            }}
            }}"""

            response = requests.post('https://graphcdn.frankenergie.nl', json={'query': query}, headers=headers)
            return response.json()
        except KeyError as e:
            log.warning(f"We did not get data from FrankEnergie api : {e}")
            return False
        except Exception as e:
            log.error(e)
            return False

    def __process_api_data(self, data:dict = None, kind:int = 1, UTC:bool = False)->dict:
        try:
            if kind == 1:
                kind = 'e'
                api_data =  data['data']['marketPricesElectricity']
            if kind == 2:
                kind = 'g'
                api_data = data['data']['marketPricesGas']

            prices = []
            for d in api_data:
                price = {}
                efrom = functions.api_general.get_timestamp(time_stamp=d['from'],UTC=UTC)
                price['fromdate'] = efrom['datum']
                price['fromtime'] = efrom['tijd']
                price['price'] = d['marketPrice']
                price['kind'] = kind
                prices.append(price)

            if prices:
                return prices

            raise KeyError('No data?')
        except KeyError as e:
            log.warning(f"We did not get data from FrankEnergie api in process_api_data : {e}")
            return False


if __name__ == "__main__":
    FE = FrankEnergie_API()
    print('Electra prijzen')
    print(FE.get_data(kind=1))
    print('Gas prijzen')
    print(FE.get_data(kind=2))