import requests
from bs4 import BeautifulSoup
import nltk
from urllib.request import urlopen
import re
import pandas as pd
import time
from newspaper import Article



headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
BASEURL_IEX='https://cloud.iexapis.com/'
BASEURL__IEX_SANDBOX = 'https://sandbox.iexapi.com/'
Token='Tpk_1bb3e623cb6342708a67c0517a71e492'
URL=BASEURL__IEX_SANDBOX+'stable/time-series/news/aapl?range=last-week&limit=1000&token='+Token
URL='https://sandbox.iexapis.com/stable/time-series/news/aapl?range=last-week&limit=10&token=Tpk_1bb3e623cb6342708a67c0517a71e492'
NASDAQ_BASE="https://www.nasdaq.com"

def get_historical_news(stocks):

    print(URL)
    json=requests.get(URL).json()

    dataframe=pd.DataFrame(json)
    print(dataframe.columns)
    dataframe['text']=dataframe['url'].apply(lambda url : url_to_text('https://cloud.iexapis.com/v1/news/article/9176b6f7-b9af-4144-9831-1eb5710be0fc'))

    #print(dataframe["url"])

    return dataframe
    #print(dataframe.head(5).url)


    #for j in json:
    #  text=url_to_text(j['url'])


'''Generalized function to get all news-related articles from a Nasdaq webpage'''


def get_news_urls_nasdaq(ticker):
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
        return news_urls

    except Exception:

        print("Exception")

    return None


def get_news_urls(links_site):

    print(links_site)
    '''scrape the html of the site'''
    resp = requests.get(links_site, headers=headers, timeout=5)


    if not resp.ok:
        return None

    html = resp.content

    '''convert html to BeautifulSoup object'''
    soup = BeautifulSoup(html, 'lxml')

    print(soup)
    '''get list of all links on webpage'''
    links = soup.find_all('a')


    urls = [link.get('href') for link in links]
    urls = [url for url in urls if url is not None]


    for url in urls:
        print(url)

    '''Filter the list of urls to just the news articles'''
    news_urls = [NASDAQ_BASE+url for url in urls if "/articles/" in url]
    time.sleep(10)
    return news_urls


def scrape_all_articles(ticker, upper_page_limit=1):
    landing_site = 'http://www.nasdaq.com/symbol/' + ticker + '/news-headlines'

    all_news_urls = get_news_urls(landing_site)
    print(all_news_urls)
    current_urls_list = all_news_urls.copy()
    index = 2

    '''Loop through each sequential page, scraping the links from each'''
    while (current_urls_list is not None) and (current_urls_list != []) and \
            (index <= upper_page_limit):
        '''Construct URL for page in loop based off index'''
        current_site = landing_site + '?page=' + str(index)
        current_urls_list = get_news_urls(current_site)

        '''Append current webpage's list of urls to all_news_urls'''
        all_news_urls = all_news_urls + current_urls_list
        print("Page  " + str (index))
        print(current_urls_list)

        index = index + 1

   # all_news_urls = list(set(all_news_urls))

    #for i,article in enumerate(all_news_urls):

    #    all_news_urls[i]=NASDAQ_BASE+article

    '''Now, we have a list of urls, we need to actually scrape the text'''
    #all_articles = [scrape_news_text(news_url) for news_url in all_news_urls]
    #text=[url_to_text(url) for url in all_news_urls]

    return all_news_urls


def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def get_url_content(url='https://cloud.iexapis.com/v1/news/article/9176b6f7-b9af-4144-9831-1eb5710be0fc'):
    print(url)

    page=requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    for script in soup(["script, style"]):
        script.extract()

    text=soup.get_text()
    raw=clean_html(page.text)
    print(raw)



def parse_urls_text(urls, ticker):

    textarray=[]

    for url in urls:
        print("Extracting:" + url)
        content, title= url_to_text(url)
        textarray.append({ 'url': url , 'content':content, 'title': title, 'ticker': ticker})

    return textarray



def url_to_text(url='https://cloud.iexapis.com/v1/news/article/9176b6f7-b9af-4144-9831-1eb5710be0fc'):

    #print(url)
    article=Article(url)
    article.download()
    article.parse()
    #print(article.text)
    #article.nlp()
    #print(article.keywords)

    return article.text, article.title



if __name__ == '__main__':


    articles=scrape_all_articles("googl", 5)
    #print(articles[-1])
    #get_historical_news("apple")
    #url_to_text()
    #get_url_content()
    for article in articles:
        print(articles)

    #data=urlopen('https://www.nasdaq.com/market-activity/stocks/sedg/news-headlines')
