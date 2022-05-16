import sys
import os
from time import time

import configparser
import logging
import logging.config

from functions_sql.tables_sql import TablesSQL
from functions.dispatcher import Dispatcher

os.environ['TZ'] = 'Europe/Amsterdam'

dir_path = os.path.dirname(os.path.realpath(__file__))
log_folder = os.path.join(dir_path, 'logging')
config_folder = os.path.join(dir_path, 'config')

os.makedirs(log_folder, exist_ok=True)

logging.config.fileConfig(os.path.join(config_folder, 'logging.conf'))

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

if PY_ENV == 'prod':
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

class EnergieBot():
    def __init__(self) -> None:
        try:
            self.config_file = os.path.join(config_folder, 'config.conf')
            if not self.check_file(file=self.config_file):
                raise Exception('Config file not found')
            self.config = None
            self.initConfig()
            self.add_extra_config()
        except Exception as e:
            log.critical(e)
            sys.exit(e)

    @staticmethod
    def check_file(file:str = "")->bool:
        if os.path.exists(file):
            return True
        return False

    def initConfig(self) -> None:
        try:
            # self.config = configparser.ConfigParser()
            self.config = configparser.RawConfigParser()
            self.config.read(self.config_file)
        except Exception as e:
            log.critical(e)
            sys.exit(e)

    def add_extra_config(self)-> None:
        try:
            startTime = int(time())
            self.config.add_section('other')
            self.config['other']['path'] = str(dir_path)
            self.config['other']['startTime'] = str(startTime)
        except KeyError as e:
            log.critical(e)
        except Exception as e:
            log.error(e)
            sys.exit(e)


if __name__ == "__main__":
    eb = EnergieBot()
    tsql = TablesSQL(dbname=eb.config['db']['name'])

    for table in ['energy', 'user']:
        tsql.no_table(table=table)
    del tsql

    D = Dispatcher(config=eb.config)
    D.start_dispatch()
