# This class will handle the integration with firestore and uploading documents to it

import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db


class FireStoreServices(object):

    def __init__(self, credentials_resource):
        self.cred = credentials.Certificate(credentials_resource)
        self.app = firebase_admin.initialize_app(self.cred,
                                                 {'databaseURL': 'https://newspector-backend.firebaseio.com/'})
        self.firestore = firestore.client()

    def add_twitter_account(self, account):
        followers = account.followers_count
        followings = account.following_count

        if followers is None:
            followers = 0

        if followings is None:
            followings = 0

        doc = self.firestore.collection('accounts').document(account.username).get()
        if doc.exists and (int(round(time.time() * 1000)) - int(
                u'{}'.format(doc.to_dict()['updated_at']))) > 172800000:  # updated 2 days ago
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
                'updated_at': int(round(time.time() * 1000))
            }
            self.firestore.collection('accounts').document(account.username).update(account_data)
        elif not doc.exists:
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
                'updated_at': int(round(time.time() * 1000)),
                'news_count': 0,
                'news_group_leadership_count': 0,
                'news_group_membership_count': 0,
                'category_map': {}
            }
            self.firestore.collection('accounts').document(account.username).set(account_data)  # to firestore db

            account_ref = db.reference('accounts')  # to realtime db
            account_ref.child(account.username).set({
                'likes_count': 0,
                'dislikes_count': 0,
                'reports_count': 0,
            })
        else:
            print("Account exists but updates are done within a 2 day period")

    def add_tweet(self, tweet):
        tweet_data = {
            'username': tweet.username,
            'userRef': self.firestore.collection("accounts").document(tweet.username),
            'tweet_id': str(tweet.tweet_id),
            'is_retweet': tweet.is_retweet,
            'date': tweet.date,
            'datestamp': tweet.datestamp,
            'timestamp': tweet.timestamp,
            'text': tweet.text,
            'tweet_link': "twitter.com/" + tweet.username + "/status/" + str(tweet.tweet_id),
            'urls': tweet.urls,
            'photos': tweet.photos,
            'video': tweet.video,
            'retweet_date': tweet.retweet_date,
            'label': tweet.label,
            'category': tweet.category,
            'perceived_category': tweet.perceived_category,
            'sentiment_score': tweet.sentiment_score,
            'report_count': 0,
            'news_group_id': "",
            'source_count_map': {},
            'keyword_map': {}
        }
        self.firestore.collection('tweets').document().set(tweet_data)
