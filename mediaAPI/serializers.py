from rest_framework import serializers
from .models import OriginMedia, UserAudio


class OriginMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginMedia
        fields = ('title', 'content', 'audio_path', 'video_path')


class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = ('user', 'origin', 'audio_path', 'score')


