import requests
from bs4 import BeautifulSoup
import nltk
from urllib.request import urlopen
import re
import pandas as pd
import time
from newspaper import Article
from data.utils import getstockspn



class Nasdaq(self):
    def __init__(self):
        self.url="https://www.nasdaq.com"
        self.articles=[]   #change to set and a
        self.stocks=getstockspn()
        self.picklefilename='./articles.plk'
        self.jsonfilename='./articles.json'
    

    def get_all_articles():
        stocks["articles"]=stocks["Symbol"].map(lambda ticker: get_news_urls_nasdaq(ticker))
        

    def save_all_articles():
        self.stocks.to_pickle(self.picklefilename)               #TODO: add datetime for a daily basis
        return

    def read_all_articles():
        self.stocks=pd.read_pickle(self.picklefilename)         #TODO: add datetime for a daily basis
        return

    def pandas_to_redis():
        pass    


    def get_news_urls_nasdaq(self, ticker):
        landing_site = 'http://www.nasdaq.com/symbol/' + ticker + '/news-headlines'
        links_site=landing_site
        print("Getting links for " + ticker)

        try:

            '''scrape the html of the site'''
            resp = requests.get(links_site, headers=headers, timeout=5)

            if not resp.ok:
                return None

            html = resp.content

            '''convert html to BeautifulSoup object'''
            soup = BeautifulSoup(html, 'lxml')

            '''get list of all links on webpage'''
            links = soup.find_all('a')

            urls = [link.get('href') for link in links]
            urls = [url for url in urls if url is not None]

            #for url in urls:
            #    print(url)

            '''Filter the list of urls to just the news articles'''
            news_urls = [NASDAQ_BASE+url for url in urls if "/articles/" in url]
            time.sleep(10)
            print("Completed")
            
            self.articles.update(news_urlss)  #TODO check if this works for updateing articles

            return news_urls

        except Exception:

            print("Exception")

        return None


    def parse_urls_text(urls, ticker):

        textarray=[]

        for url in urls:
            print("Extracting:" + url)
            textarray.append({ 'url': url , 'content': url_to_text(url), 'ticker': ticker})

        return textarray

    def url_to_text(url='https://cloud.iexapis.com/v1/news/article/9176b6f7-b9af-4144-9831-1eb5710be0fc'):

        #print(url)
        article=Article(url)
        article.download()
        article.parse()
        #print(article.text)
        #article.nlp()
        #print(article.keywords)

        return article.text     

    def extract_articles(self)
    
        self.stocks["Newscontent"]= ''
        newdata=[]
        for i, row in articles.iterrows():
            content=parse_urls_text(row["articles"], row["Symbol"])
            stocks.at[i, "Newscontent"]=content
            newdata.append(content)


