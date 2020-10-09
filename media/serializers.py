"""
Serializers for media app
"""
from rest_framework import serializers
from .models import OriginMedia, UserAudio


class OriginMediaSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """
    class Meta:
        model = OriginMedia
        fields = ('title', 'content', 'audio_path', 'video_path')


class UserAudioSerializer(serializers.ModelSerializer):
    """
    serialize UserAudio data
    """
    class Meta:
        model = UserAudio
        fields = ('user', 'origin', 'audio_path', 'score')
