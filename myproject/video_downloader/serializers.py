# video_downloader/serializers.py
from rest_framework import serializers
from .models import VideoAudio

class VideoAudioSerializer(serializers.ModelSerializer):
    audio_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoAudio
        fields = ['id', 'video_url', 'name', 'audio_file', 'audio_file_url', 'created_at']
        read_only_fields = ['audio_file', 'created_at']
    
    def get_audio_file_url(self, obj):
        if obj.audio_file:
            return obj.audio_file.url
        return None

class VideoAudioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAudio
        fields = ['video_url', 'name']