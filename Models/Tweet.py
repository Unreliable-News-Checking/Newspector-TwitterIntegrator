# This is the model class of a news
import re
from datetime import datetime


def get_date_in_millis(date):
    dt_obj = datetime.strptime(str(date),
                               '%Y-%m-%d %H:%M:%S')
    return dt_obj.timestamp() * 1000


class Tweet(object):

    # instance attributes
    def __init__(self, username, tweet_id, is_retweet, date, text, urls,
                 photos, video, retweet_date, datestamp, timestamp,
                 category, sentiment_score):
        self.username = username
        self.tweet_id = tweet_id
        self.is_retweet = is_retweet
        self.date = date
        self.datestamp = datestamp
        self.timestamp = timestamp
        self.text = text
        self.urls = urls
        self.photos = photos
        self.video = video
        self.retweet_date = retweet_date,
        self.category = category
        self.perceived_category = category
        self.sentiment_score = sentiment_score
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
