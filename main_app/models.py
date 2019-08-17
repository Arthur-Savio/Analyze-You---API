from django.db import models


class ChannelDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='')
    subs = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    profile_image_link = models.CharField(max_length=200, default='')


class VideoDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    tags = models.TextField(default='')


class Statistics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sentiment_result = models.TextField(default='')
    time_series = models.TextField(default='')
    word_cloud = models.TextField(default='')
