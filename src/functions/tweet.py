import os
import logging

import tweepy

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Tweet:
    def __init__(self, *args, **kwargs) -> None:
        config = kwargs['config']
        __twit_conf = self.get_twitter_keys(config=config)
        self.__api_key = __twit_conf['api_key']
        self.on = int(__twit_conf['on'])
        self.__api_key_secret = __twit_conf['api_key_secret']
        self.__access_token = __twit_conf['access_token']
        self.__access_token_secret = __twit_conf['access_token_secret']
        self.__bearer_token = __twit_conf['bearer_token']
        self.__client = None
        pass

    def get_twitter_keys(self,config:dict = None)->dict:
        try:
            match PY_ENV:
                case 'dev':
                    return config['twitter_dev']
                case 'acc':
                    return config['twitter_dev']
                case 'prod':
                    return config['twitter_prod']
                case _:
                    return config['twitter_dev']

        except KeyError as e:
            log.error(e, exc_info=True)
        except Exception as e:
            log.critical(e, exc_info=True)

    def __tweet_connect(self)->None:
        try:
            self.__client =  tweepy.Client(bearer_token=self.__bearer_token,
            consumer_key=self.__api_key, consumer_secret=self.__api_key_secret,
            access_token=self.__access_token, access_token_secret=self.__access_token_secret
            )

            return True
        except Exception as e:
            log.critical("Error creating CLIENT ", exc_info=True)
            return False

    def tweettie(self, msg:str = None)->bool:
        try:
            if not self.on: #do not run
                return True

            if msg is None:
                return False

            if self.__tweet_connect():

                response = self.__client.create_tweet(text=msg, user_auth=True)
                return True

            return False
        except Exception as e:
            log.critical("Error creating Tweet ", exc_info=True)
            return False
