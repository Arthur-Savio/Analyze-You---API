from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .models import *
from .serializer import *
from .resources.api_requests import ApiRequests


class ChannelDetailsView(APIView):
    """This get return details about a specific channel"""
    def get(self, request, format=None):
        api_requests = ApiRequests(request.query_params.get('video_link'))
        response = api_requests.get_channel_details()
        return Response(response)


class VideoDetailsView(APIView):
    """This get return details about a specific video"""
    def get(self, request, format=None):
        api_requests = ApiRequests(request.query_params.get('video_link'))
        response = api_requests.get_video_details()
        return Response(response)


class StatisticsView(APIView):
    """This get receive a video link and return statistics about it"""
    def get(self, request, format=None):
        api_requests = ApiRequests(request.query_params.get('video_link'))
        response = api_requests.get_comments_and_generate_plots()
        return Response(response)

    def post(self, data):
        serializer = StatisticsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, format=None):
        queryset = Statistics.objects.all()
        serializer = StatisticsSerializer(queryset, many=True)

        for i in serializer.data:
            pk = dict(i)
            element = Statistics.objects.get(pk=pk['id'])
            element.delete()
        return Response(serializer.data)
