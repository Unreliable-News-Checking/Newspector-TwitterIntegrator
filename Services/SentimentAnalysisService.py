from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from func_timeout import func_set_timeout


class SentimentAnalysisService:
    def __init__(self):
        self.compound_Score_threshold = 0.05

    @func_set_timeout(10)
    def get_sentiment_from_text(self, text):

        if type(text) is not str:
            return 0.0

        analyzer = SentimentIntensityAnalyzer()
        testimonial = TextBlob(text)

        sentiment_1 = testimonial.sentiment
        sentiment_2 = analyzer.polarity_scores(text)

        return (sentiment_1.polarity + sentiment_2["compound"]) / 2

        # compound_score = sentiment_2['compound']
        # if compound_score >= self.compound_Score_threshold:
        #     sentiment_2_overall = 'positive'
        # elif compound_score > -self.compound_Score_threshold and self.compound_Score_threshold < 0.05:
        #     sentiment_2_overall = 'neutral'
        # else:
        #     sentiment_2_overall = 'negative'

        # print(f'sentiment 1: {sentiment_1}, sentiment 2: {sentiment_2} overall: {sentiment_2_overall}')
        # return sentiment_2_overall
