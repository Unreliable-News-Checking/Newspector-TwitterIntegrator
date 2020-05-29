from datetime import datetime
import twint
import json
import os
from Utilities.DateOperations import get_date_in_millis


class TwitterServices:

    def __init__(self, accounts_resource, user_tweet_map_resource, breaking_news_tags_resource):
        self.accounts_resource = accounts_resource  # sets the path for the resource
        self.user_tweet_map_resource = user_tweet_map_resource
        self.user_tweet_map = self.load_map_from_resources(self.user_tweet_map_resource)
        self.accounts_map = self.load_map_from_resources(self.accounts_resource)
        with open(breaking_news_tags_resource) as f:
            self.breaking_news_tags = json.load(f)

    def save_map_to_resources(self, user_tweet_map, resource):
        with open(resource, 'w') as outfile:
            json.dump(user_tweet_map, outfile)

    def load_map_from_resources(self, path):
        if os.stat(path).st_size == 0:
            return None
        else:
            with open(path) as json_file:
                return json.load(json_file)

    def update_map(self, account_name, last_fetched_date):  # updates the map after fetch operation on source  done
        return self.user_tweet_map.update({account_name: last_fetched_date})

    def fetch_latest_tweets_from_account(self, account_name, last_fetched_date):
        tweets = []
        dt = str(
            datetime.fromtimestamp((last_fetched_date - 86400000) / 1000.0))  # start search form 1 day before
        conf = twint.Config()
        twint.output.clean_lists()
        conf.Username = account_name
        conf.Since = dt[0:19]
        conf.Store_object = True
        conf.Hide_output = True

        twint.run.Search(conf)
        tweets += twint.output.tweets_list
        twint.output.clean_lists()

        conf.Native_retweets = True
        twint.run.Search(conf)
        tweets += twint.output.tweets_list
        twint.output.clean_lists()

        result = []
        for tweet in tweets:
            if get_date_in_millis(tweet.datestamp + " " + tweet.timestamp) > last_fetched_date:
                if self.accounts_map[account_name]:
                    # if the account is a general news account only retrieve breaking news
                    for tag in self.breaking_news_tags:
                        text = tweet.tweet
                        if text.lower().find(tag.lower()) >= 0:
                            result.append(tweet)
                            break
                else:
                    result.append(tweet)

            # Add breaking tag filtering for necessary accounts
        return result

    def fetch_account_info(self, account_name):
        conf = twint.Config()
        conf.Username = account_name
        conf.Limit = 1
        conf.Hide_output = True
        conf.Pandas = True
        twint.run.Lookup(conf)
        account = twint.storage.panda.User_df
        twint.storage.panda.clean()
        return account
