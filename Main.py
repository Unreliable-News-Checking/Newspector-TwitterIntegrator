import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import ServerApplication
import time


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


# cred = credentials.Certificate("Resources/service-account-file.json")
# app = firebase_admin.initialize_app(cred,
#                                                  {'databaseURL': 'https://newspector-backend.firebaseio.com/'})
# firestore = firestore.client()
#
# cities_ref = firestore.collection(u'tweets')
#
# docs = cities_ref.where(u'username', u'==', "FRANCE24").stream()
#
# for doc in docs:
#     firestore.collection('tweets').document(doc.id).delete()