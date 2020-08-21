import pandas as pd 
from numpy import random
import numpy as np
from recommender.data.Stocks import getstockinfo

#TODO: load all this from a config file

DATADIR='/home/jehill/PycharmProjects/recommendersystem/recommender/data/jsons/'

def random_sample(arr, size = 5): 
    print(arr[1])
    return arr[np.random.choice(len(arr), size=size, replace=False)]


def getrandomarticles(ticker,article_df, max=10):
   n=random.randint(low=3, high=max)

   data=article_df.loc[article_df['Symbol'] == ticker ]
   articles=data['articles'].values
   arr=articles[0]
   randomselection=np.random.choice(arr, size=min(n,len(arr)))

   return randomselection


def getarticles(ticker, article_df):

   data=article_df.loc[article_df['Symbol'] == ticker ]
   articles=data['articles'].values[0]

   return articles

def getallarticles(tickers, articles_df):
    article_list = []

    for ticker in tickers:
      article_list = np.concatenate([article_list, getarticles(ticker, articles_df)])

    return article_list

def getrandomstocks(stocktickers, max=30):
   n=random.randint(low=10, high=max)
   randomstocks=random.choice(stocktickers, size=n)
   
   return randomstocks


def gettrainingdata(number_users, stocktickers ):

   userdata=[]

   for user in range(number_users):

      stocks=getrandomstocks(stocktickers)
      article_list=[]

      for ticker in stocks:

         article_list=np.concatenate([article_list, getrandomarticles(ticker,articles_df)])

      print("User= "  + str(user)  + "Number of articles" + str(len(article_list)) )
      user={"userid": user, "articles": article_list, "stocks": stocks}

      userdata.append(user)

   usersdf=pd.DataFrame(data=userdata)
   print(usersdf.head(10))
   #usersdf.to_json(DATADIR+ "userdata.json")

   return usersdf


def get_test_data( training_data, articles_df, fraction=0.3):

    test_dataframe=training_data.sample(frac=0.3)

    test_data=[]

    for index, user in test_dataframe.iterrows():
       print(user["userid"])
       articles=user["articles"]
       tickers=user["stocks"]
       article_list = []

       for ticker in tickers:
          article_list = np.concatenate([article_list, getrandomarticles(ticker, articles_df)])

       test_articles=list(set(article_list)-set(articles))
       print("Test articles:" + str(len(test_articles)))
       print("Train articles:" + str(len(articles)))

       user = {"userid": user["userid"], "articles": test_articles, "stocks": tickers}
       test_data.append(user)

    print("number of training data points"  + str(len(test_data)))

    return pd.DataFrame(data=test_data)


if __name__ == '__main__':

  articles_df=pd.read_json(DATADIR + 'Nasdaq_articles')
  stocktickers=articles_df["Symbol"].values
  number_users=100
  userdata=[]
  count=0



  #train_dataframe=get_training_data(number_users, stocktickers)
  #train_dataframe.to_json(DATADIR + "userdata.json")

  train_dataframe=pd.read_json(DATADIR + "userdata.json")
   
  test_dataframe=get_test_data(train_dataframe, articles_df)
  test_dataframe.to_json(DATADIR + "testdata.json")




