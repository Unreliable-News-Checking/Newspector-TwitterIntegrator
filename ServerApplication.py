import json

from Models import TwitterAccount
from Models import Tweet
from Services import TwitterServices, CategorizationService, SentimentAnalysisService
from Services import FirestoreServices
from Controllers import ModelController


class ServerApplication(object):

    def __init__(self, accounts_resource, user_tweet_map_resource, firestore_credentials_resource, stop_words_resource,
                 category_subcategory_map_resource):
        self.accounts_resource = accounts_resource
        self.user_tweet_map_resource = user_tweet_map_resource
        self.category_subcategory_map_resource = category_subcategory_map_resource
        self.firestore_credentials_resource = firestore_credentials_resource
        self.stop_words_resource = stop_words_resource
        self.twitter_service = TwitterServices.TwitterServices(self.accounts_resource, self.user_tweet_map_resource)
        self.firestore_service = FirestoreServices.FireStoreServices(self.firestore_credentials_resource)
        self.model_controller = ModelController.ModelController()
        self.categorization_service = CategorizationService.CategorizationService(
            self.category_subcategory_map_resource)
        self.sentiment_analysis_service = SentimentAnalysisService.SentimentAnalysisService()

        with open(self.stop_words_resource) as f:
            self.stop_words = json.load(f)

    def run(self):
        self.download_accounts()
        self.download_tweets()

        # do any operation needed on models
        self.filter_tweets_from_accounts()
        # do any operation needed on models

        self.upload_accounts()
        self.upload_tweets()

    def download_tweets(self):
        for i in self.twitter_service.user_tweet_map:
            tweets = self.twitter_service.fetch_latest_tweets_from_account(i,
                                                                           self.twitter_service.user_tweet_map[i])
            index = tweets.index

            if len(index) != 0:
                last_tweet_date = 0
                for index, tweet in tweets.iterrows():

                    if len(tweet["urls"]) > 0:
                        print(tweet["urls"][0])

                        try:
                            category = self.categorization_service.get_category(
                                tweet["urls"][0])
                        except:
                            category = "-"

                        try:
                            sentiment_score = self.sentiment_analysis_service.get_sentiment_from_text(
                                self.categorization_service.extract_content(tweet["urls"][0]))
                        except:
                            sentiment_score = 0.0
                    else:
                        category = "-"
                        sentiment_score = self.sentiment_analysis_service.get_sentiment_from_text(tweet["tweet"])

                    print(
                        "Account: " + i + " , Category:" + category + " , Sentiment:" + str(
                            sentiment_score) + " , ID: " + str(
                            tweet["id"]))

                    t = Tweet.Tweet(i, tweet["id"], tweet["retweet"], tweet["timestamp"],
                                    tweet["tweet"], tweet["replies_count"], tweet["retweets_count"],
                                    tweet["likes_count"],
                                    tweet["urls"],
                                    tweet["photos"],
                                    tweet["video"], tweet["hashtags"], tweet["cashtags"], tweet["source"],
                                    tweet["created_at"],
                                    tweet["retweet_date"],
                                    tweet["user_rt_id"], tweet["link"], tweet["datestamp"], tweet["place"],
                                    tweet["timezone"], category, sentiment_score)

                    self.model_controller.add_tweet_to_account(t, i)

                    if not tweet["retweet"]:
                        if int(tweet["timestamp"]) > last_tweet_date:
                            last_tweet_date = int(tweet["timestamp"])
                    else:
                        if int(tweet["retweet_date"]) > last_tweet_date:
                            last_tweet_date = int(tweet["retweet_date"])

                self.twitter_service.update_map(i, last_tweet_date)
            print("Tweets fetched from " + i)

    def upload_tweets(self):
        for account in list(self.model_controller.get_accounts().values()):
            for tweet in account.get_tweets():
                self.firestore_service.add_tweet(tweet)
            print("Tweets uploaded from " + account.username)
        self.twitter_service.save_map_to_resources(self.twitter_service.user_tweet_map, self.user_tweet_map_resource)

    def download_accounts(self):
        for username in self.twitter_service.user_tweet_map:
            profile = self.twitter_service.fetch_account_info(username)
            account = TwitterAccount.TwitterAccount(username, profile["name"].iloc[0], profile["followers"].iloc[0],
                                                    profile["following"].iloc[0],
                                                    profile["likes"].iloc[0], profile["tweets"].iloc[0],
                                                    profile["url"].iloc[0],
                                                    profile["avatar"].iloc[0],
                                                    profile["join_date"].iloc[0], profile["bio"].iloc[0], list())
            self.model_controller.add_or_update_account(account)
            print("Account info for " + username + " fetched")

    def upload_accounts(self):
        for account in list(self.model_controller.get_accounts().values()):
            self.firestore_service.add_twitter_account(account)
            print("Account info uploaded for " + account.username)

    def filter_tweets_from_accounts(self):
        for account in list(self.model_controller.get_accounts().values()):
            account.filter_tweets(self.stop_words)
            print("Tweets filtered for " + account.username + " fetched")
