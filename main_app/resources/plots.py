import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pandas.plotting import register_matplotlib_converters
import dateutil
import statistics
import seaborn as sn
from wordcloud import WordCloud

register_matplotlib_converters()


class Plots:
    """This class generate the graphics to statistics analyzes."""

    def sentiment_plot(self, list):
        """This method generate a screw plot contain the information about sentiments
        express in comments. The graphic are composed of bad and good feelings. """

        labels = ['Negative','Positive']
        colors = ['lightcoral','lightskyblue']

        circle = plt.Circle((0,0), 0.7, color='white')

        plt.pie(list, labels=labels, colors=colors, wedgeprops={'linewidth':7, 'edgecolor':'white'})
        p = plt.gcf()
        p.gca().add_artist(circle)
        plt.savefig('staticfiles/sentiment.png')

    def time_series_plot(self, date_list, all_polarity):
        """This method is more complex. This generate a time series plot, that simulates
        the feelings variation in turn of the dates. The Y axis contain the dates and X axis
        contain the variation of feelings."""

        plt.clf()
        my_dict = self.treat_date(date_list, all_polarity)

        sn.set_context('paper')
        sn.set_style('whitegrid')
        sn.despine()

        dates_neg = [dateutil.parser.parse(i) for i in my_dict.keys()]
        dates_pos = dates_neg

        xmft = md.DateFormatter('%Y-%m-%d')
        ax = plt.gca()
        ax.xaxis.set_major_formatter(xmft)
        plt.xticks(rotation=25)

        new_polarity_list = dict()
        new_polarity_list['negative'] = [statistics.mean(i['negative']) for i in my_dict.values() if len(i['negative']) > 0]
        new_polarity_list['positive'] = [statistics.mean(i['positive']) for i in my_dict.values() if len(i['positive']) > 0]

        if len(new_polarity_list['negative']) != len(dates_neg):
            x = len(dates_neg) - len(new_polarity_list['negative'])
            dates_neg = dates_neg[:len(dates_neg) - x]
        plt.plot(dates_neg, new_polarity_list['negative'], label='Negative', color='red')

        if len(new_polarity_list['positive']) != len(dates_pos):
            x = len(dates_pos) - len(new_polarity_list['positive'])
            dates_pos = dates_pos[:len(dates_pos) - x]
        plt.plot(dates_pos, new_polarity_list['positive'], label='Positive', color='dodgerblue')

        plt.ylabel("Polarity")
        plt.xlabel("Date")
        plt.legend()
        plt.savefig('staticfiles/time_series.png')

    @staticmethod
    def treat_date(date_list, all_polarity):
        """This method treat the dates and converted to a friendly format."""

        my_dict = dict()

        for i in date_list:
            date = i.split('T')[0]
            my_dict[date] = dict()
            my_dict[date]['negative'] = list()
            my_dict[date]['positive'] = list()

        for i in range(len(all_polarity)):
            date = date_list[i].split('T')[0]

            if all_polarity[i] < 0:
                my_dict[date]['negative'].append(all_polarity[i])
            elif all_polarity[i] > 0:
                my_dict[date]['positive'].append(all_polarity[i])
        return my_dict

    def word_cloud(self, words):
        """This method was created to generate a friendly graphic to represents the words that
        have the most occurrence in the comments."""

        plt.clf()
        words = ' '.join(words)
        wordcloud = WordCloud(background_color='white').generate(words)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('staticfiles/word_cloud.png')
