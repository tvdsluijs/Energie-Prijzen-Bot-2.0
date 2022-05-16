from datetime import datetime
import os
import logging

import psutil

from telegram.utils.helpers import escape_markdown

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Systeem():
    def __init__(self) -> None:
        pass

    def systeminfo_msg(self, dt:str=None, version:str=None, dbname:str = None, users:int = None, seconds:int = None)->str:
        try:
            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime(("%Y-%m-%d %H:%M"))

            sysinfo = f"""
System time : {vandaag}
Bot version : {version}
Database :    {self.fileSize(dbname)}
Uptime :      {self.secondsToText(seconds)}
Users :       {users}
CPU load :    {self.get_cpu_usage_pct()}%
RAM usage:    {int(self.get_ram_usage() / 1024 / 1024)} MB
"""
            sysinfo = escape_markdown(sysinfo, version=2)
            msg = f"""

Systeem informatie:
```
{sysinfo}
```
Dit systeem is gebouwd onder MIT license\. Je kan de code op Github vinden 'Energie\-Prijzen\-Bot\-2\.0'
"""
            return msg

        except Exception as e:
            log.error(e)

    def fileSize(self, filePath):
        try:
            size = os.path.getsize(filePath)
            return self.unitConvertor(size)
        except Exception as e:
            log.error(e)

    # some other functions
    @staticmethod
    def unitConvertor(sizeInBytes):
        try:
            #Cinverts the file unit
            if sizeInBytes < 1024*1024:
                size = round(sizeInBytes/1024)
                return f"{size} KB"
            elif sizeInBytes < 1024*1024*1024:
                size = round(sizeInBytes/(1024*1024))
                return f"{size} MB"
            elif sizeInBytes >= 1024*1024*1024:
                size = round(sizeInBytes/(1024*1024*1024))
                return f"{size} GB"
            else:
                return f"{sizeInBytes} Bytes"
        except Exception as e:
            log.error(e)


    @staticmethod
    def get_ram_usage():
        return int(psutil.virtual_memory().total - psutil.virtual_memory().available)

    @staticmethod
    def get_cpu_usage_pct():
        return psutil.cpu_percent(interval=0.5)

    @staticmethod
    def secondsToText(unit, granularity = 2):
        try:
            ratios = {
                'decennia' : 311040000, # 60 * 60 * 24 * 30 * 12 * 10
                'jaar'   : 31104000,  # 60 * 60 * 24 * 30 * 12
                'maanden'  : 2592000,   # 60 * 60 * 24 * 30
                'dagen'    : 86400,     # 60 * 60 * 24
                'uur'   : 3600,      # 60 * 60
                'minuten' : 60,        # 60
                'seconden' : 1          # 1
            }

            texts = []
            for ratio in ratios:
                result, unit = divmod(unit, ratios[ratio])
                if result:
                    if result == 1:
                        ratio = ratio.rstrip('s')
                    texts.append(f'{result} {ratio}')
            texts = texts[:granularity]
            if not texts:
                return f'0 {list(ratios)[-1]}'
            text = ', '.join(texts)
            if len(texts) > 1:
                index = text.rfind(',')
                text = f'{text[:index]}, {text[index + 1:]}'
            return text
        except Exception as e:
            log.error(e)