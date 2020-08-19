import pandas as pd
import numpy as np
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import sklearn
import scipy


DATADIR='/home/jehill/PycharmProjects/recommendersystem/recommender/data/jsons/'
USERFILE= DATADIR + 'userdata.json'
ARTICLEFILE= DATADIR +  'article.json'

if __name__ == '__main__':


   articles=json.load(open(ARTICLEFILE))
   articles_df=pd.DataFrame.from_dict((articles), orient="index")
   print(articles_df.head(5))

   stopwords_list=stopwords.words('english')

   item_ids=articles_df['articleid'].tolist()

   vectorizer=TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df=0.0003, max_df=0.95, max_features=7500, stop_words=stopwords_list)
   tfidf_matrix=vectorizer.fit_transform(articles_df["content"]+ " " +articles_df["title"])
   feature_names=vectorizer.get_feature_names()
   print(np.shape(feature_names))
   print(feature_names[100:600])


   def get_item_profile(item_id):
       idx = item_ids.index(item_id)
       item_profile = tfidf_matrix[idx:idx + 1]
       return item_profile


   def get_item_profiles(ids):
       item_profiles_list = [get_item_profile(x) for x in ids]
       item_profiles = scipy.sparse.vstack(item_profiles_list)
       return item_profiles

   a=get_item_profile(10)
   #print(a)

   hashmap = {}
   for article in articles:
       a = articles[article]
       hashmap[a["url"]] = a


   def get_user_profile(urls):

       article_ids=[]

       for url in urls:
           article_ids.append(hashmap[url]["articleid"])

       user_item_profiles=get_item_profiles(article_ids)
       user_profile_norms=sklearn.preprocessing.normalize(np.sum(user_item_profiles,axis=0))

       return user_profile_norms
   
   userdata = pd.read_json(USERFILE)
   #print(userdata.head(5))

   p=get_user_profile(userdata.loc[50].articles)

   p=p.flatten().tolist()
   print(p[:100])
   print(np.shape(p))

   data=sorted(zip(p,feature_names), key=lambda  x: -x[0])

   usercontent=pd.DataFrame(data, columns=["relvance", "token"] )

   print(usercontent.head(10))



