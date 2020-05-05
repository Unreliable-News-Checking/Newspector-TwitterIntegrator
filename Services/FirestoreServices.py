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

        if followers is None:
            followers = 0

        if followings is None:
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
                'birthday': account.birthday
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
                'news_count': 0,
                'news_group_leadership_count': 0,
                'news_group_membership_count': 0,
                'like_count': 0,
                'dislike_count': 0,
                'category_map': {}
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
            'video': tweet.video,
            'hashtags': tweet.hashtags,
            'cashtags': tweet.cashtags,
            'source': tweet.source,
            'created_at': tweet.created_at,
            'retweet_date': tweet.retweet_date,
            'user_rt_id': tweet.user_rt_id,
            'link': tweet.link,
            'datestamp': tweet.datestamp,
            'place': tweet.place,
            'timezone': tweet.timezone,
            'label': tweet.label,
            'category': tweet.category,
            'perceived_category': tweet.perceived_category,
            'sentiment_score': tweet.sentiment_score,
            'report_count': 0,
            'news_group_id': "",
            'source_count_map': {},
            'keyword_map': {}
        }
        self.db.collection('tweets').document().set(tweet_data)
