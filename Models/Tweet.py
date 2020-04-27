# This is the model class of a news
import re


class Tweet(object):

    # instance attributes
    def __init__(self, username, tweet_id, is_retweet, date, text, reply_count, retweet_count, likes, urls,
                 photos, videos, category):
        self.username = username
        self.tweet_id = tweet_id
        self.is_retweet = is_retweet
        self.date = date
        self.text = text
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.likes = likes
        self.urls = urls
        self.photos = photos
        self.videos = videos
        self.category = category
        self.perceived_category = category
        self.label = ""

    def filter(self, stop_words):
        is_label_set = False
        for url in self.urls:
            self.text = re.sub(url, "", self.text)
        self.text = re.sub(r"http\S+", "", self.text)
        self.text = re.sub(r"pic.twitter.com\S+", "", self.text)
        for word in stop_words:
            if self.text.lower().find(word.lower()) >= 0:
                self.text = re.sub(word, "", self.text, flags=re.IGNORECASE)
                if is_label_set is False:
                    self.label = re.sub(r'[^a-zA-Z0-9]+', "", word)
                    is_label_set = True
        self.text = re.sub("BREAKING ", "", self.text)  # Source bazlı filtering e geçince CASE Sensitive yapıcaz
        self.text = re.sub("…", "", self.text, flags=re.IGNORECASE)
        self.text = ' '.join(self.text.split())
