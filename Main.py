import ServerApplication
import time

# We can move these resource paths to a config file

accounts_resource = "Resources/AccountNames.json"
user_tweet_map_resource = "Resources/UserTweetIDMap.json"
firestore_credentials_resource = "Resources/service-account-file.json"
filter_resource = "Resources/stop_words.json"

server_app = ServerApplication.ServerApplication(accounts_resource, user_tweet_map_resource,
                                                 firestore_credentials_resource, filter_resource)

var = 1
while var == 1:  # This constructs an infinite loop
    server_app.run()
    time.sleep(120)

# import json
# import re
#
# text = "LIVE VIDEO: fksmfşlsakflisjfsnfljksl ..."
#
# with open('Resources/stop_words.json') as f:
#     stop_words = json.load(f)
#
# for word in stop_words:
#     if text.lower().find(word.lower()) >= 0:
#         text = re.sub(r"http\S+", "", text)
#         text = re.sub(r"pic.twitter.com\S+", "", text)
#         text = re.sub("[\.][\.][\.]", " ", text)
#         for word in stop_words:
#             if text.lower().find(word.lower()) >= 0:
#                 label = re.sub(r'[^a-zA-Z0-9]+', "", word)
#                 text = re.sub(word, "", text, flags=re.IGNORECASE)
#         text = re.sub("BREAKING ", "", text)  # kötü bir practice ama yapacak bir şey yok
# print(text)
# print(label)