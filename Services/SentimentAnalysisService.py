from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalysisService:
    def __init__(self):
        self.compound_Score_threshold = 0.05

    def get_sentiment_from_text(self, text):
        # burda iki tane library var kullandigimiz
        # sentiment 1 ve 2 diye ayirdim
        # 1. libraryi polarity veriyo negatif -1, positif 1 ara degerlerde verbiliyor
        # bide subjectivity veriyo 0 ila 1 arasi
        # 2. library negatif neutral positif yuzdeleri veriyor bide compound skor veriyo
        # libraryi yazanlar >= 0.05 e positif
        # -0.05 ve 0.05 arasi neutral
        # <= -0.05 e negatif demis
        # bunlari bir sekilde harmanlayabiliriz ya da test edelim hangisi iyiyse onu kullanalim

        analyzer = SentimentIntensityAnalyzer()
        testimonial = TextBlob(text)

        sentiment_1 = testimonial.sentiment
        sentiment_2 = analyzer.polarity_scores(text)

        compound_score = sentiment_2['compound']
        if compound_score >= self.compound_Score_threshold:
            sentiment_2_overall = 'positive'
        elif compound_score > -self.compound_Score_threshold and self.compound_Score_threshold < 0.05:
            sentiment_2_overall = 'neutral'
        else:
            sentiment_2_overall = 'negative'

        # print(f'sentiment 1: {sentiment_1}, sentiment 2: {sentiment_2} overall: {sentiment_2_overall}')
        return sentiment_2_overall
