# This is the model class of a news
import re


class Tweet(object):

    # instance attributes
    def __init__(self, username, tweet_id, is_retweet, time, text, reply_count, retweet_count, likes, urls,
                 photos, videos):
        self.username = username
        self.tweet_id = tweet_id
        self.is_retweet = is_retweet
        self.time = time
        self.text = text
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.likes = likes
        self.urls = urls
        self.photos = photos
        self.videos = videos
        self.label = ""

    def filter(self, stop_words):
        for url in self.urls:
            self.text = re.sub(url, "", self.text)
        self.text = re.sub(r"http\S+", "", self.text)
        self.text = re.sub(r"pic.twitter.com\S+", "", self.text)
        self.text = re.sub("[\.][\.][\.]", " ", self.text)
        for word in stop_words:
            if self.text.lower().find(word.lower()) >= 0:
                self.label = word
                self.text = re.sub(word, "", self.text, flags=re.IGNORECASE)
