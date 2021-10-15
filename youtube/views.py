from django.shortcuts import render
import requests
from .endpoints import ENDPOINTS
from django.conf import settings
from django.urls import reverse 
from django.http import HttpResponseRedirect
from .models import User
from django.core.cache import cache

def search_video(request):
    if request.POST:
        name = request.POST['video_name']
        videos = requests.get(ENDPOINTS['GET_VIDEOS_LIST'](name)).json()
        #print(videos)
        video_ids = ','.join(map(lambda video:video['id']['videoId'], videos['items']))
        video_statistics = requests.get(ENDPOINTS['GET_VIDEOS_STATISTIC'](video_ids)).json()
        for index in range(len(videos['items'])):
            videos['items'][index]['statistics']=video_statistics['items'][index]['statistics']
        context = {'videos' : videos['items']}
        return render(request, 'youtube/show_video.html', context)
    else:
        context = {'login_url': ENDPOINTS['AUTH_USER'], 'token': cache.get('token')}
        #print(context)
        return render(request, 'youtube/search_video.html', context)

def get_comments(request, video_id):
    if request.POST:
        comment_text = request.POST['comment']
        token = cache.get('token')
        #print(token)
        data = {
            "snippet": {
                "channelId": "UCvnHWUOceExXV831E_ToyAA",
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
        #print(data)
        response = requests.post(ENDPOINTS['POST_COMMENTS'](token), json=data).json() 
        #print(response)  
        return HttpResponseRedirect(reverse('get_comments', args=[video_id]))
    else:
        if cache.get('token'):
            user_info = requests.get(ENDPOINTS['GET_USER_INFO'](cache.get('token')))
            print(user_info)
        comments = requests.get(ENDPOINTS['GET_COMMENTS'](video_id)).json()
        #print(comments)
        if 'error' in comments and comments['error']['code'] == 403 and comments['error']['errors'][0]['reason']== 'commentsDisabled':
            context = {'comments_disabled' : True, 'video_id' : video_id}  
        else:
            context = {'comments': comments['items'], 'video_id' : video_id}  
        return render(request,'youtube/comments.html', context)
        
def login(request):
    code = request.GET['code']
    data = {'client_id': settings.YOUTUBE_CLIENT_ID,
            'client_secret': settings.YOUTUBE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://127.0.0.1:8000/login'
            }
    response = requests.post(ENDPOINTS['GET_TOKEN'], data=data).json()
    #user_info = requests.get(ENDPOINTS['GET_USER_INFO'](response['access_token'])).json()
    #print(user_info)
    cache.get_or_set('token', response['access_token'])
    #print(response)
    return HttpResponseRedirect(reverse('search_video'))

def logout(request):
    cache.delete('token')
    return HttpResponseRedirect(reverse('search_video'))




   

