# video_downloader/api_urls.py
from django.urls import path
from .api_views import VideoAudioCreateAPIView, VideoAudioListAPIView

urlpatterns = [
    path('create/', VideoAudioCreateAPIView.as_view(), name='api-audio-create'),
    path('list/', VideoAudioListAPIView.as_view(), name='api-audio-list'),
]