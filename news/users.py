import pandas as pd 
from numpy import random


if __name__ == '__main__':

   p=pd.read_json('/Users/jehill/Documents/code/git/recommender-system/news/Nasdaq_articles')
   print(p["articles"].head(5))