"""
models for media app
"""
# pylint: disable=E5142
import os
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class OriginMedia(models.Model):
    """
    model of original media
    """
    level_id = models.IntegerField(unique=True, db_index=True)
    speaker_id = models.CharField(max_length=64, null=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)  # 文案, 格式可能修改
    audio_path = models.FileField(max_length=256, upload_to='origin/audio/')
    video_path = models.FileField(max_length=256, upload_to='origin/video/')


@receiver(pre_delete, sender=OriginMedia)
def auto_delete_file_on_delete(instance: OriginMedia, **_):
    """
    delete file from file system when the object is deleted
    """
    if instance.audio_path and os.path.isfile(instance.audio_path.path):
        os.remove(instance.audio_path.path)
    if instance.video_path and os.path.isfile(instance.video_path.path):
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
    if not video_old == video_new and os.path.isfile(video_old.path):
        os.remove(video_old.path)
    if not audio_old == audio_new and os.path.isfile(audio_old.path):
        os.remove(audio_old.path)
