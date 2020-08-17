from news.data.News.utils import *
from news.Stocks import getstocktickers


if __name__ == '__main__':

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
