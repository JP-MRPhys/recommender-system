from typing import List, Any

import pandas as pd
import numpy as np
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import sklearn
import scipy
from recommender.model.evaluation import ModelEvaluator

#TODO: load all this from a config file

DATADIR='/home/jehill/PycharmProjects/recommendersystem/recommender/data/jsons/'
TRAINFILE= DATADIR + 'userdata.json'
TESTFILE= DATADIR + 'testdata.json'
ARTICLEFILE= DATADIR +  'article.json'
STOCKFILE = DATADIR + 'Nasdaq_articles'

class ContentBasedRecommender:
    MODEL_NAME = 'Content-Based-News-Aritcles'

    def __init__(self, items_dict=None):

        self.articles=items_dict
        self.items_df = pd.DataFrame.from_dict((items_dict), orient="index")
        self.stopwords_list = stopwords.words('english')

        self.item_ids = self.items_df['articleid'].tolist()
        self.url_hashmap=self.get_url_hashmap(self.articles)  #TO DO organise this better creating this to get user data for users from items dataframe

        self.vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0003, max_df=0.95, max_features=7500,
                                     stop_words=self.stopwords_list)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.items_df["content"] + " " + self.items_df["title"])
        self.feature_names = self.vectorizer.get_feature_names()

        print("completed creating the following recommender: " + self.MODEL_NAME)

    def get_model_name(self):
        return self.MODEL_NAME

    def _get_similar_items_to_user_profile(self, user_profiles, topn=25):
        # Computes the cosine similarity between the user profile and all item profiles
        cosine_similarities = cosine_similarity(user_profiles, self.tfidf_matrix)
        # Gets the top similar items
        similar_indices = cosine_similarities.argsort().flatten()[-topn:]
        # Sort the similar items by similarity
        similar_items = sorted([(self.item_ids[i], cosine_similarities[0, i]) for i in similar_indices], key=lambda x: -x[1])
        return similar_items

    def recommend_items(self, userurls, items_to_ignore=[], topn=10, verbose=False):

        user_profile=self.get_user_profile(userurls)
        similar_items = self._get_similar_items_to_user_profile(user_profile)
        # Ignores items the user has already interacted
        similar_items_filtered = list(filter(lambda x: x[0] not in items_to_ignore, similar_items))  # this is a list (article_id, similarity)
        recommended_urls=self.similar_items_to_urls(similar_items_filtered)

        return recommended_urls

    def similar_items_to_urls(self, similar_items_filtered):

            recommended_urls=[]

            for item in similar_items_filtered:
                article_id=item[0] #index of the dataframe
                url=self.items_df.iloc[article_id].url  #TODO check whether index in dataframe is same as article id
                recommended_urls.append(url)

            return recommended_urls


    def get_item_profile(self,item_id):
        idx = self.item_ids.index(item_id)
        item_profile = self.tfidf_matrix[idx:idx + 1]
        return item_profile

    def get_item_profiles(self, ids):
        item_profiles_list = [self.get_item_profile(x) for x in ids]
        item_profiles = scipy.sparse.vstack(item_profiles_list)
        return item_profiles

    def get_user_profile(self,  user_urls):

        # must be one user
        # user profile from training dataframe urls

        #urls=user_dataframe["articles"]
        urls=user_urls

        article_ids = []

        for url in urls:

          try:
            article_ids.append(self.url_hashmap[url]["articleid"])
          except Exception:
              print("Not founds " + url)


        user_item_profiles = self.get_item_profiles(article_ids)
        user_profile_norms = sklearn.preprocessing.normalize(np.sum(user_item_profiles, axis=0))

        return user_profile_norms

    def get_url_hashmap(self, articles):

        hashmap = {}
        for article in articles:
            a = articles[article]
            hashmap[a["url"]] = a

        return hashmap


if __name__ == '__main__':

    articles_url = json.load(open(ARTICLEFILE))
    articles_df = pd.DataFrame.from_dict((articles_url), orient="index")
    recommender=ContentBasedRecommender(articles_url)

    stocks_df=pd.read_json(open(STOCKFILE))


    model_evaluator=ModelEvaluator(stocks_df)

    user_training_data=pd.read_json(TRAINFILE)
    user_test_data=pd.read_json(TESTFILE)



    final_metric, detail_metric= model_evaluator.evaluate_model(recommender, user_training_data, user_test_data)

    print(final_metric)

    print(detail_metric.head(10))
    for i in range(10):

     #print(user_training_data.loc[i])
     training_articles=user_training_data.loc[i]["articles"]
     recommendation=recommender.recommend_items(training_articles)
     #print(recommendation)
    
    
    
