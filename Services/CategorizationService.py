# # Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from boilerpy3 import extractors
# from multi_rake import Rake
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
            "Resources/category-extraction-service-key.json"

class CategorizationService:

    def __init__(self):
        # self.rake = Rake()
        self.extractor = extractors.ArticleExtractor()
        self.client = language.LanguageServiceClient()


    def extract_content(self, url):
        content = self.extractor.get_content_from_url(url)
        content = content.replace("\n", "").replace("\"", "")
        content = content[:999]
        return content

    def get_categories(self, text: str):
        # The text to analyze
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        categories = self.client.classify_text(document=document)
        return categories

    # def get_keywords(text: str, num_keywords: int):
    #     keywords = rake.apply(text)
    #     return keywords[:num_keywords]

    def get_category_and_keywords(self, url):
        content = self.extract_content(url)
        categories = self.get_categories(content)
        # keywords = get_keywords(content, 5)
        return categories
        # return categories, keywords
