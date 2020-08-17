import pandas as pd 
import numpy as np

iexconfig={'baseurl': 'https://cloud.iexapis.com/'  , 
           'sandboxurl': 'https://sandbox.iexapis.com/stable/' , 
           'sandboxtoken': 'Tpk_1bb3e623cb6342708a67c0517a71e492', 
           'token':  'pk_eb4172c3df4e42a09206514386c44fcd', 
           'topsurl':  }


class iex:
    def __init__(self, iexconfig, redisconfig):

        self.iexconfig=iexconfig['token']
        self.stocks=get_tops()
        

    def get_tops()

    def get_stock_list()    

    def get_market_news()

    def get_stock_news(self, ticker, range)
        url=config['baseurl'] + 'time-series/news/' + ticker + '?+range='+ range + 'limit=25&token=' +  config['sandboxtoken']

        #URL='time-series/news/aapl?range=last-week&limit=10&token=Tpk_1bb3e623cb6342708a67c0517a71e492'


    def get_last_quote()

    def update_stock_quote()
        self.stock_get_tops()

    def cache_market_data():


    def store_DB():