from .connect_api import ConnectApi
from .data_cleaning import DataCleaning
from .model import Model
from .sentiment_analysis import SentimentAnalysis
from .plots import Plots


class ApiRequests:
    """These class provide a methods that make and return requests from Youtube API """
    def __init__(self, video_link):
        self.video_link = video_link
        self.connect_api = ConnectApi(self.video_link)

    def get_comments_and_generate_plots(self):
        """The get comments method make a request and receive all comments from video. This comments
        are used to realize the main purpose of this API, that is analyze and generate statistics
        data about a video. After receive the data, this method call others methods that work with these comments"""

        self.connect_api = ConnectApi(self.video_link)
        data_cleaning = DataCleaning()
        self.connect_api.get_video_comments()
        data_cleaning.steps_control_to_cleaning_dataset(self.connect_api.all_comments)

        sentiment = SentimentAnalysis(data_cleaning.tokens_list)
        sentiment.analysis()

        # model = Model()
        # model.load_model()
        #
        # result = model.make_prediction(data_cleaning.all_comments).tolist()
        # predict_results = [result.count('0'), result.count('1')]

        statistics = Plots()
        statistics.sentiment_plot(sentiment.polarity_data)
        statistics.time_series_plot(self.connect_api.comments_date, sentiment.all_polarity)
        statistics.word_cloud(data_cleaning.all_words)

        return {
            'sentiment_result':'https://api-analyzeyou.herokuapp.com/static/sentiment.png',
            'time_series':'https://api-analyzeyou.herokuapp.com/static/time_series.png',
            'word_cloud':'https://api-analyzeyou.herokuapp.com/static/word_cloud.png',
            'predict_results':sentiment.polarity_data
        }

    def get_channel_details(self):
        """This method receive details about channel. This channel is the channel that contain the video
        analyzed. The details are: Title, Subs, Views, Profile image.

        These data isn't important to statistics but is necessary to build high informations about the video and
        the channel.
        """
        channel_id = self.connect_api.get_video_details()[0]['snippet']['channelId']
        response = self.connect_api.get_channel_details(channel_id)[0]

        return {
            'title':response['snippet']['title'],
            'subs':response['statistics']['subscriberCount'],
            'views':response['statistics']['viewCount'],
            'profile_image_link':response['snippet']['thumbnails']['default']['url']
        }

    def get_video_details(self):
        """This method follow the same ideia of get_channel_details method. The difference is that receive
        different informations."""
        response = self.connect_api.get_video_details()[0]

        return {
            'title':response['snippet']['title'],
            'description':response['snippet']['description'],
            'tags':', '.join(response['snippet']['tags']),
            'thumbnails':response['snippet']['thumbnails']['default']['url']
        }


