from recommender.data.utils import *
from recommender.data.Stocks import getstockinfo
from recommender.data.News import url_to_text
import json

DATADIR='/home/jehill/PycharmProjects/recommendersystem/recommender/data/jsons/'
ARTRICLE_FILE= DATADIR + 'article.json'

if __name__ == '__main__':





    stocks=pd.read_json(DATADIR+'Nasdaq_articles')
    print(len(stocks))
    articles={}
    articleid=1;

    for i, row in stocks.iterrows():



        urls=row["articles"]
        ticker=row["Symbol"]

        for j, url in enumerate(urls):
            if url not in articles.keys():

              try:

                 content, title=url_to_text(url)
                 article={'url': url, 'content': content, 'title': title, 'ticker': ticker, 'articleid': articleid}

                 print(title)
                 articles[url]=article
                 articleid+=1

              except Exception:

                  print("Exception while downloading articles")


    json.dump(articles, open (ARTRICLE_FILE, "w"))

    #read json
    data=json.load(open(ARTRICLE_FILE))

    """
       #download articles:

          stocks=getstocktickers()
       print(stocks.head(5))
       stocks=stocks.head(200)
       stocks["articles"]=stocks["Symbol"].map(lambda ticker: get_news_urls_nasdaq(ticker))
       stocks.to_json("Nasdaq_articles")

       #print(stocks.head(3))
       #print(articles["articles"].head(5))
       #articles["NewsContent"]=articles["articles"].map(lambda urls: parse_urls_text(urls))

       articles=pd.read_json("Nasdaq_articles")
       articles["Newscontent"]= ''
       newdata=[]

       for i, row in articles.iterrows():

           print(i)



           content=parse_urls_text(row["articles"], row["Symbol"])
           articles.at[i, "Newscontent"]=content
           newdata.append(content)

           print(content)


       articles["Newscontent"]=newdata
       articles.to_json("Nasdaq_newsContent")

    """