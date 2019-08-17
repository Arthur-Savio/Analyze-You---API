import requests

class ConnectApi:
    """The methods just be requests to Youtube Api"""
    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = self.video_url.split('=')[1]
        self.key = 'YOUR KEY'
        self.all_comments = list()
        self.comments_date = list()

    def get_channel_details(self, id):
        response = requests.get('https://www.googleapis.com/youtube/v3/channels',
                                params={'part':'snippet, statistics',
                                        'id':id,
                                        'key':self.key})
        return response.json()['items']

    def get_video_details(self):
        response = requests.get('https://www.googleapis.com/youtube/v3/videos',
                                params={'part':'snippet',
                                        'id':self.video_id,
                                        'key':self.key})

        return response.json()['items']

    def get_video_comments(self):
        count = 0
        first_response = requests.get('https://www.googleapis.com/youtube/v3/commentThreads',
                                      params={'part':'snippet',
                                              'videoId':self.video_id,
                                              'key':self.key,
                                              'maxResults':100})

        first_response.connection.close()
        next_page_token = first_response.json()['nextPageToken']
        self.append_list(first_response)

        while True:
            response = requests.get('https://www.googleapis.com/youtube/v3/commentThreads',
                                    params={'part': 'snippet',
                                            'videoId': self.video_id,
                                            'key': self.key,
                                            'maxResults': 100,
                                            'pageToken': next_page_token})
            count += 100
            print(count)
            if 'nextPageToken' in response.json():
                next_page_token = response.json()['nextPageToken']
                self.append_list(response)
            else:
                self.append_list(response)
                response.connection.close()
                break

    def append_list(self, response):
        for i in range(0, len(response.json()['items'])):
            self.comments_date.append(response.json()['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt'])
            self.all_comments.append(response.json()['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
