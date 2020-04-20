# This is the model class of a news source which will store news and other related information about the source
class TwitterAccount(object):

    # instance attributes
    def __init__(self, username, name, followers_count, following_count, likes_count, tweets_count, website,
                 profile_photo, birthday, bio, tweet_list):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.likes_count = likes_count
        self.tweets_count = tweets_count
        self.website = website
        self.profile_photo = profile_photo
        self.birthday = birthday
        self.bio = bio
        self.tweet_list = tweet_list

    def add_tweets(self, tweets):
        self.tweet_list.append(tweets)

    def set_tweets(self, tweets):
        self.tweet_list = tweets

    def get_tweets(self):
        return self.tweet_list

    def filter_tweets(self, stop_words):
        for tweet in self.get_tweets():
            tweet.filter(stop_words)
