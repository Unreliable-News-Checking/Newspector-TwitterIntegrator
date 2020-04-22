# This class will handle the integration with firestore and uploading documents to it

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FireStoreServices(object):

    def __init__(self, credentials_resource):
        self.cred = credentials.Certificate(credentials_resource)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def add_twitter_account(self, account):
        followers = account.followers_count
        followings = account.following_count

        if followers == 1:
            followers = followings
            followings = 0

        if self.db.collection('accounts').document(account.username).get().exists:
            account_data = {
                'username': account.username,
                'name': account.name,
                'followers_count': followers,
                'following_count': followings,
                'likes_count': account.likes_count,
                'tweets_count': account.tweets_count,
                'website': account.website,
                'profile_photo': account.profile_photo,
                'birthday': account.birthday,
            }
            self.db.collection('accounts').document(account.username).update(account_data)
        else:
            account_data = {
                'username': account.username,
                'name': account.name,
                'followers_count': followers,
                'following_count': followings,
                'likes_count': account.likes_count,
                'tweets_count': account.tweets_count,
                'website': account.website,
                'profile_photo': account.profile_photo,
                'birthday': account.birthday,
                'number_of_total_news': 0,
                'number_of_first_news_in_group': 0,
                'number_of_reports': 0,
                'number_of_approvals': 0
            }
            self.db.collection('accounts').document(account.username).set(account_data)

    def add_tweet(self, tweet):
        tweet_data = {
            'username': tweet.username,
            'userRef': self.db.collection("accounts").document(tweet.username),
            'tweet_id': tweet.tweet_id,
            'is_retweet': tweet.is_retweet,
            'date': tweet.date,
            'text': tweet.text,
            'reply_count': tweet.reply_count,
            'retweet_count': tweet.retweet_count,
            'tweet_link': "twitter.com/" + tweet.username + "/status/" + tweet.tweet_id,
            'likes': tweet.likes,
            'urls': tweet.urls,
            'photos': tweet.photos,
            'videos': tweet.videos,
            'label': tweet.label,
            'news_group_id': tweet.news_group_id,
            'category': tweet.category
        }
        self.db.collection('train_tweets').document().set(tweet_data)
