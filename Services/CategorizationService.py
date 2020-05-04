import json
import signal
from contextlib import contextmanager
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from boilerpy3 import extractors
import os
from func_timeout import func_set_timeout

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "Resources/category-extraction-service-key.json"


class CategorizationService:

    def __init__(self, category_subcategory_map_resource):
        self.extractor = extractors.LargestContentExtractor()
        self.client = language.LanguageServiceClient()
        with open(category_subcategory_map_resource) as json_file:
            self.map = json.load(json_file)

    def extract_content(self, url):
        try:
            content = self.extractor.get_content_from_url(url)
        except:
            return None
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

    @func_set_timeout(10)
    def get_category(self, url):
        category = "-"

        content = self.extract_content(url)

        if content is None:
            return category

        try:
            categories = self.get_categories(content).categories
        except:
            categories = None

        if categories:
            category = categories[0].name.split("/")[1]
            if category == "News":
                category = self.map[categories[0].name[1:]]
            else:
                try:
                    category = self.map[categories[0].name.split("/")[1]]
                except:
                    print("Map does not have key: " + categories[0].name.split("/")[1])

        return category
