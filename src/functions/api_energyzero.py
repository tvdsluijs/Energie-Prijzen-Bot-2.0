import os
from datetime import datetime, timedelta

import functions.api_general
import requests

import logging

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class EnergieZero_API:

    def __init__(self) -> None:
        pass

    def get_data(self, startdate:str = "", enddate:str = "", kind:int = 1)->dict:
        try:
            api_data = self.__get_api_data(startdate=startdate, enddate=enddate, kind=kind)
            if (data := self.__process_api_data(data=api_data, kind=kind, UTC=True)):
                 return data

            raise KeyError('No Data?')
        except KeyError as e:
            log.warning(f"We did not get data from EnergyZero api : {e}")
            return False
        except Exception as e:
            log.error(e)
            return False

    def __get_api_data(self, startdate:str = "", enddate:str = "", kind:int = 1)->dict:
        try:
            if startdate == "":
                yesterday_ts = datetime.now() + timedelta(days=-1)
                startdate = yesterday_ts.strftime("%Y-%m-%d")
            if enddate == "":
                tomorrow_ts = datetime.now() + timedelta(days=+1)
                enddate = tomorrow_ts.strftime("%Y-%m-%d")

            # interval=4 => dag
            # interval=9 => Week
            # interval=5 => Maand
            # interval=6 => Jaar
            url = f"https://api.energyzero.nl/v1/energyprices?fromDate={startdate}T00%3A00%3A00.000Z&tillDate={enddate}T23%3A59%3A59.999Z&interval=4&usageType={kind}&inclBtw=false"
            response = requests.get(url)
            return response.json()
        except KeyError as e:
            log.warning(f"We did not get data from EnergyZero api : {e}")
            return False
        except Exception as e:
            log.error(e)
            return False

    def __process_api_data(self, data:dict = None, kind:int = 1, UTC:bool = False)->dict:
        try:
            if kind == 1:
                kind = 'e'
            if kind == 2:
                kind = 'g'

            api_data = data['Prices']

            prices = []
            for d in api_data:
                price = {}
                efrom = functions.api_general.get_timestamp(time_stamp=d['readingDate'],UTC=UTC)
                price['fromdate'] = efrom['datum']
                price['fromtime'] = efrom['tijd']
                price['price'] = d['price']
                price['kind'] = kind

                prices.append(price)

            if prices:
                return prices

            raise KeyError('No data?')
        except KeyError as e:
            log.warning(f"We did not get data from EnergyZero api in process_api_data : {e}")
            return False

if __name__ == "__main__":
    EZ = EnergieZero_API()
    print('Electra prijzen')
    print(EZ.get_data(kind=2))
    print('Gas prijzen')
    print(EZ.get_data(kind=1))