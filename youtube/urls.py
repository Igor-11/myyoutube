from django.urls import path
from . import views

urlpatterns = [
    path('search-video', views.search_video, name='search_video'),
    path('comments/<video_id>', views.get_comments, name='get_comments'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('', views.search_video, name='search_video'),
]