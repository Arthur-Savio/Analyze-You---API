from rest_framework import serializers
from .models import *


class ChannelDetailsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ChannelDetailsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = ChannelDetails
        fields = ('id', 'title', 'subs', 'views', 'profile_image_link')


class VideoDetailsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(VideoDetailsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = VideoDetails
        fields = ('id', 'title', 'description', 'tags')


class StatisticsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(StatisticsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Statistics
        fields = ('id', 'sentiment_result', 'time_series', 'word_cloud')