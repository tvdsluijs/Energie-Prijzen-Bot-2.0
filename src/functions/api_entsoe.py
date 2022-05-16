import os
import json
from datetime import datetime, timedelta

from entsoe import EntsoePandasClient
import pandas as pd

import functions.api_general

import logging

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class Entsoe_API:
    def __init__(self) -> None:
        pass

    def get_data(self, startdate:str="", enddate:str="", entsoe_key:str=None)->dict:
        try:
            if entsoe_key is None or entsoe_key == "":
                raise Exception("We don't have a entsoe key")

            api_data = self.__get_api_data(startdate=startdate, enddate=enddate, entsoe_key=entsoe_key)

            # kind is always 1 = Energy!
            if (data := self.__process_api_data(data=api_data, kind=1,  UTC=False)):
                 return data

            raise KeyError('No Data?')
        except KeyError as e:
            log.warning(f"We did not get data from EnergyZero api : {e}")
            return False
        except Exception as e:
            log.error(e)
            return False

    def __get_api_data(self, startdate:str = "", enddate:str = "", entsoe_key:str=None)->json:
        try:
            if startdate == "":
                yesterday = datetime.now() + timedelta(days=-1)
                periodStart = yesterday.strftime("%Y%m%d0001") #yyyyMMddHHmm
            if enddate == "":
                tomorrow = datetime.now() + timedelta(days=+1)
                periodEnd = tomorrow.strftime("%Y%m%d2359") #yyyyMMddHHmm

            startdate = pd.Timestamp(periodStart, tz='Europe/Brussels')
            enddate = pd.Timestamp(periodEnd, tz='Europe/Brussels')
            data = {}
            client = EntsoePandasClient(api_key=entsoe_key)

            country_code = 'NL'
            ts = client.query_day_ahead_prices(country_code,start=startdate,end=enddate)
            return ts.to_dict()

        except Exception as e:
            log.error(e)
            return False

    def __process_api_data(self, data:dict = None, kind:int = 1, UTC:bool = False)->dict:
        try:
            if kind == 1:
                kind = 'e'
            if kind == 2:
                kind = 'g'

            prices = []
            for k,v in data.items():
                price = {}
                dt = pd.to_datetime(k)
                efrom = functions.api_general.get_timestamp(time_stamp=dt,UTC=UTC)
                price['fromdate'] = efrom['datum']
                price['fromtime'] = efrom['tijd']
                price['price'] = float(v/1000)
                price['kind'] = kind
                prices.append(price)

            if prices:
                return prices

            raise KeyError('No data?')
        except KeyError as e:
            log.warning(f"We did not get data from EnergyZero api in process_api_data : {e}")
            return False

if __name__ == "__main__":
    EN = Entsoe_API()
    print('Electra prijzen')
    print(EN.get_data(entsoe_key=""))

