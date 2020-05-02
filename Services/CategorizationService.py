import json
import signal
from contextlib import contextmanager
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from boilerpy3 import extractors
import os
import time

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

    @contextmanager
    def timeout(self, time_amount):
        # Register a function to raise a TimeoutError on the signal.
        signal.signal(signal.SIGALRM, self.raise_timeout)

        signal.alarm(time_amount)

        try:
            yield
        except TimeoutError:
            pass
        finally:
            # Unregister the signal so it won't be triggered
            # if the timeout is not reached.
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

    def raise_timeout(self, signum, frame):
        raise TimeoutError
