# video_downloader/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from .serializers import VideoAudioSerializer, VideoAudioCreateSerializer
from .models import VideoAudio
from .utils import download_audio
import os
from django.core.files import File
import logging

logger = logging.getLogger(__name__)

class VideoAudioListAPIView(ListAPIView):
    queryset = VideoAudio.objects.all().order_by('-created_at')
    serializer_class = VideoAudioSerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoAudioCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = VideoAudioCreateSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            name = serializer.validated_data['name']
            
            try:
                if VideoAudio.objects.filter(video_url=video_url).exists():
                    return Response(
                        {"error": "Video URL already processed"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                audio_file_path = download_audio(video_url, name)
                if not audio_file_path:
                    return Response(
                        {"error": "Failed to download audio"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                try:
                    video_audio = VideoAudio(video_url=video_url, name=name)
                    with open(audio_file_path, 'rb') as f:
                        video_audio.audio_file.save(f"{name}.mp3", File(f))
                    video_audio.save()
                    
                    os.remove(audio_file_path)
                    
                    return Response({
                        "message": "Audio downloaded and saved successfully",
                        "video_url": video_url,
                        "name": name,
                        "audio_file": video_audio.audio_file.url
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Error saving audio file: {str(e)}")
                    if audio_file_path and os.path.exists(audio_file_path):
                        os.remove(audio_file_path)
                    return Response(
                        {"error": f"Failed to save audio file: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                logger.error(f"Unexpected error in audio processing: {str(e)}")
                return Response(
                    {"error": f"Unexpected error: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)