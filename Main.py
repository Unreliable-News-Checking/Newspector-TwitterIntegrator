from datetime import datetime

import ServerApplication
import time
import twint

# Parameters
accounts_resource = "Resources/all_accounts.json"
user_tweet_map_resource = "Resources/user_date_map.json"
firestore_credentials_resource = "Resources/service-account-file.json"
stop_words_resource = "Resources/stop_words.json"
breaking_news_tags_resource = "Resources/breaking_news_tags.json"
category_subcategory_map_resource = "Resources/category_subcategory_map.json"

server_app = ServerApplication.ServerApplication(accounts_resource, user_tweet_map_resource,
                                                 firestore_credentials_resource, stop_words_resource,
                                                 breaking_news_tags_resource,
                                                 category_subcategory_map_resource
                                                 )

var = 1
while var == 1:  # This constructs an infinite loop
    server_app.run()
    time.sleep(60)
