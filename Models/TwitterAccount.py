import numpy as np


# This is the model class of a news source which will store news and other related information about the source


class TwitterAccount(object):

    # instance attributes
    def __init__(self, username, name, followers_count, following_count, likes_count, tweets_count, website,
                 profile_photo, birthday, bio):
        self.username = username
        self.name = name
        self.followers_count = int(followers_count)
        self.following_count = int(following_count)
        self.likes_count = int(likes_count)
        self.tweets_count = int(tweets_count)
        self.website = website.replace("http://", "https://")
        self.profile_photo = profile_photo
        self.birthday = birthday
        self.bio = bio
        self.tweet_list = []

    def add_tweets(self, tweets):
        self.tweet_list.append(tweets)

    def set_tweets(self, tweets):
        self.tweet_list = tweets

    def get_tweets(self):
        return self.tweet_list

    def filter_tweets(self, stop_words):
        for tweet in self.get_tweets():
            tweet.filter(stop_words)
