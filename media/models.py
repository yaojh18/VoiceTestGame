"""
models for media app
"""
# pylint: disable=E5142
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class OriginMedia(models.Model):
    """
    model of original media
    """
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)  # 文案, 格式可能修改
    audio_path = models.FileField(max_length=256, upload_to='origin/audio/')
    video_path = models.FileField(max_length=256, upload_to='origin/video/')


class UserAudio(models.Model):
    """
    model of user audio
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.ForeignKey(OriginMedia, on_delete=models.CASCADE)
    audio_path = models.FileField(max_length=256, upload_to='user/audio/')
    score = models.FloatField()


@receiver(pre_delete, sender=OriginMedia)
def auto_delete_file_on_delete(instance: OriginMedia, **_):
    """
    delete file from file system when the object is deleted
    """
    print('pre_delete')
    if instance.audio_path:
        print('delete audio:', instance.audio_path)
        if os.path.isfile(instance.audio_path.path):
            os.remove(instance.audio_path.path)
    if instance.video_path:
        if os.path.isfile(instance.video_path.path):
            os.remove(instance.video_path.path)


@receiver(pre_save, sender=OriginMedia)
def auto_delete_file_on_change(instance: OriginMedia, **_):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return

    try:
        video_old = OriginMedia.objects.get(pk=instance.pk).video_path
        audio_old = OriginMedia.objects.get(pk=instance.pk).audio_path
    except OriginMedia.DoesNotExist:
        return

    video_new = instance.video_path
    audio_new = instance.audio_path
    if not video_old == video_new:
        if os.path.isfile(video_old.path):
            print('delete video')
            os.remove(video_old.path)
    if not audio_old == audio_new:
        if os.path.isfile(audio_old.path):
            os.remove(audio_old.path)
