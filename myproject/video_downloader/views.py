# video_downloader/views.py
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import VideoAudio

def custom_logout_view(request):
    """Custom logout view to handle logout functionality"""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'video_downloader/home.html'
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_audios'] = VideoAudio.objects.all().order_by('-created_at')[:5]
        return context

class AudioDownloadListView(LoginRequiredMixin, ListView):
    model = VideoAudio
    template_name = 'video_downloader/audio_list.html'
    context_object_name = 'audio_files'
    paginate_by = 10
    ordering = ['-created_at']
    login_url = reverse_lazy('login')