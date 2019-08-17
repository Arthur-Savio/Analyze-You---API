from textblob import TextBlob


class SentimentAnalysis:
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list
        self.polarity_data = [0, 0]
        self.all_polarity = list()

    def analysis(self):
        for i in self.tokens_list:
            comment = ' '.join(i)
            if len(comment) > 0:
                analysis = TextBlob(comment)
                polarity = analysis.sentiment.polarity

                self.all_polarity.append(polarity)

                if polarity < 0:
                    self.polarity_data[0] += 1
                elif polarity > 0:
                    self.polarity_data[1] += 1
