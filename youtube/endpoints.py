from django.conf import settings


BASE_URL = 'https://www.googleapis.com/youtube/v3/'
ENDPOINTS = {
    'GET_VIDEOS_LIST': lambda video_name: BASE_URL + 'search?type=video&q=' + video_name + '&key='+ settings.YOUTUBE_API_KEY, 
    'GET_VIDEOS_STATISTIC': lambda video_ids: BASE_URL + 'videos?part=statistics&id=' + video_ids + '&key='+ settings.YOUTUBE_API_KEY,
    'GET_COMMENTS': lambda video_id: BASE_URL + 'commentThreads?part=snippet&order=time&textFormat=plainText&videoId='+ video_id + '&key='+ settings.YOUTUBE_API_KEY,
    'POST_COMMENTS': lambda token: BASE_URL + 'commentThreads?part=snippet&access_token='+ token,
    'AUTH_USER': f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl&access_type=offline&include_granted_scopes=true&state=state_parameter_passthrough_value&redirect_uri=http%3A%2F%2F127.0.0.1:8000%2Flogin&client_id={settings.YOUTUBE_CLIENT_ID}',
    'GET_TOKEN': 'https://oauth2.googleapis.com/token',
    'GET_USER_INFO': lambda token: f'https://accounts.google.com/o/oauth2/v1/userinfo?alt=json&access_token=' + token

    }
