# we chose Recall@N as the evaluation matrix other recommendations are the NDCG@N and MAP@N


import random
from recommender.data.users import getallarticles
# Top-N accuracy metrics consts
EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = 50
import pandas as pd

class ModelEvaluator:

    def __init__(self, articles_df):

        self.articles_df=articles_df
        print("Completed creating evaluator")
    # matrix is use Recall@N

    def get_not_interacted_items_sample(self, test_data, tickers, sample_size, seed=42):
        interacted_items=set(test_data)
        all_items = set(getallarticles(tickers,self.articles_df))  #TODO  avoid pass a new agrement or via database
        non_interacted_items = all_items - interacted_items
        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, k=sample_size)
        return set(non_interacted_items_sample)

    def _verify_hit_top_n(self, item_id, recommended_items, topn):
        try:
            index = next(i for i, c in enumerate(recommended_items) if c == item_id)
        except:
            index = -1
        hit = int(index in range(0, topn))
        return hit, index

    def evaluate_model_for_user(self, model, person_id,train_data, test_data, tickers):
        # Getting the items in test set

        person_interacted_items_testset = set(test_data)

        interacted_items_count_testset = len(person_interacted_items_testset)

        # Getting a ranked recommendation list from a model for a given user
        recommended_urls = model.recommend_items(train_data,
                                               items_to_ignore=train_data,
                                               topn=100)

        hits_at_5_count = 0
        hits_at_10_count = 0
        # For each item the user has interacted in test set
        for item_id in person_interacted_items_testset:
            # Getting a random sample (100) items the user has not interacted
            # (to represent items that are assumed to be no relevant to the user)
            non_interacted_items_sample = self.get_not_interacted_items_sample(test_data, tickers,
                                                                               sample_size=EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS)

            # Combining the current interacted item with the 100 random items
            items_to_filter_recs = non_interacted_items_sample.union(set([item_id]))

            # Filtering only recommendations that are either the interacted item or from a random sample of 100 non-interacted items
            valid_recs = [url for url in recommended_urls if url in items_to_filter_recs] #person_recs_df[person_recs_df['contentId'].isin(items_to_filter_recs)]
            #valid_recs = valid_recs_df['contentId'].values
            # Verifying if the current interacted item is among the Top-N recommended items
            hit_at_5, index_at_5 = self._verify_hit_top_n(item_id, valid_recs, 5)
            hits_at_5_count += hit_at_5
            hit_at_10, index_at_10 = self._verify_hit_top_n(item_id, valid_recs, 10)
            hits_at_10_count += hit_at_10

        # Recall is the rate of the interacted items that are ranked among the Top-N recommended items,
        # when mixed with a set of non-relevant items
        recall_at_5 = hits_at_5_count / float(interacted_items_count_testset)
        recall_at_10 = hits_at_10_count / float(interacted_items_count_testset)

        metrics = {'hits@5_count': hits_at_5_count,
                          'hits@10_count': hits_at_10_count,
                          'interacted_count': interacted_items_count_testset,
                          'recall@5': recall_at_5,
                          'recall@10': recall_at_10}
        return metrics

    def evaluate_model(self, model, training_dataframe, test_dataframe):
        # print('Running evaluation for users')
        people_metrics = []
        #for idx, person_id in enumerate(list(interactions_test_indexed_df.index.unique().values)):

        count=0;

        for index, row in test_dataframe.iterrows():
             count+=1

             user_id=row["userid"]
             train_data_user=training_dataframe.loc[training_dataframe["userid"]==user_id]
             test_articles=row["articles"]
             train_articles=train_data_user["articles"].values[0]  #TODO: need to sort this out for reading from dataframe

             person_metrics = self.evaluate_model_for_user(model, user_id, train_articles,test_articles, row["stocks"])
             person_metrics['userid'] = user_id
             people_metrics.append(person_metrics)

        print('%d users processed' % count)





        detailed_results_df = pd.DataFrame(people_metrics) \
            .sort_values('interacted_count', ascending=False)

        global_recall_at_5 = detailed_results_df['hits@5_count'].sum() / float(
            detailed_results_df['interacted_count'].sum())
        global_recall_at_10 = detailed_results_df['hits@10_count'].sum() / float(
            detailed_results_df['interacted_count'].sum())

        global_metrics = {'modelName': model.get_model_name(),
                          'recall@5': global_recall_at_5,
                          'recall@10': global_recall_at_10}
        return global_metrics, detailed_results_df





if __name__ == '__main__':


    print("test")