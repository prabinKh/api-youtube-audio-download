# video_downloader/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomeView, AudioDownloadListView, custom_logout_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('audio-list/', AudioDownloadListView.as_view(), name='audio-list'),
    
    path('login/', auth_views.LoginView.as_view(template_name='video_downloader/login.html'), name='login'),
    path('logout/', custom_logout_view, name='custom-logout'),  # Custom logout view to fix the issue
    
    path('api/audio/', include('video_downloader.api_urls')),
]