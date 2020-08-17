import pandas as pd 
from numpy import random
from Stocks import getstockinfo
import numpy as np

def random_sample(arr, size = 5): 
    print(arr[1])
    return arr[np.random.choice(len(arr), size=size, replace=False)]


def getrandomarticles(ticker, stockdataframe, max=10):
   n=random.randint(low=3, high=max)

   data=stockdataframe.loc[stockdataframe['Symbol'] == ticker ]
   articles=data['articles'].values
   arr=articles[0]
   randomselection=np.random.choice(arr, size=min(n,len(arr)))

   return randomselection


def getrandomstocks(stocktickers, max=30):
   n=random.randint(low=10, high=max)
   randomstocks=random.choice(stocktickers, size=n)
   
   return randomstocks


if __name__ == '__main__':

   p=pd.read_json('/Users/jehill/Documents/code/git/recommender-system/news/Nasdaq_articles')
   stocktickers=p["Symbol"].values
   numbersusers=100
   userdata=[]
   count=0

   art=getrandomarticles("MMM", p)
   #for a in art:
   #   print("aaaaaaaa")
   #   print(a)

   
   for user in range(numbersusers):
      
      stocks=getrandomstocks(stocktickers)
      article_list=[]

      for ticker in stocks:

         article_list=np.concatenate([article_list, getrandomarticles(ticker,p)])

      print("User= "  + str(user)  + "Number of articles" + str(len(article_list)) )
      user={"userid": user, "articles": article_list, "stocks": stocks}   

      userdata.append(user)
   
   usersdf=pd.DataFrame(data=userdata)
   print(usersdf.head(10))
   usersdf.to_json("/Users/jehill/Documents/code/git/recommender-system/news/data/userdata.json")








