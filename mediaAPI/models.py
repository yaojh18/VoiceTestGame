from django.db import models
from django.contrib.auth.models import User


class OriginMedia(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)  # 文案, 格式可能修改
    audio_path = models.FileField(max_length=256, upload_to='origin/audio/')
    video_path = models.FileField(max_length=256, upload_to='origin/video/')


class UserAudio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.ForeignKey(OriginMedia, on_delete=models.CASCADE)
    audio_path = models.FileField(max_length=256, upload_to='user/audio/')
    score = models.FloatField()

