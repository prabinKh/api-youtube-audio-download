
# video_downloader/models.py
from django.db import models

class VideoAudio(models.Model):
    video_url = models.URLField(max_length=500, unique=True)
    name = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name