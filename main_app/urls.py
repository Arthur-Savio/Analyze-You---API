from django.urls import path
from main_app import views

urlpatterns = [
    path('channel_details/', views.ChannelDetailsView.as_view()),
    path('video_details/', views.VideoDetailsView.as_view()),
    path('statistics/', views.StatisticsView.as_view()),
]