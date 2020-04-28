import ServerApplication
import time

# We can move these resource paths to a config file

# Parameters
accounts_resource = "Resources/AccountNames.json"
user_tweet_map_resource = "Resources/UserTweetIDMap.json"
firestore_credentials_resource = "Resources/service-account-file.json"
filter_resource = "Resources/stop_words.json"
category_subcategory_map_resource = "Resources/Category_SubCategory_map.json"
page_count_for_account = 5

server_app = ServerApplication.ServerApplication(accounts_resource, user_tweet_map_resource,
                                                 firestore_credentials_resource, filter_resource,
                                                 category_subcategory_map_resource,
                                                 page_count_for_account)

var = 1
while var == 1:  # This constructs an infinite loop
    server_app.run()
    time.sleep(120)
