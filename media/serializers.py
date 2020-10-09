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
        fields = "__all__"
        # fields = ('title', 'content', 'audio_path', 'video_path')

    def update(self, old_data):
        old_data.title = self.title
        old_data.content = self.content
        old_data.audio_path = self.audio_path
        old_data.video_path = self.video_path
        old_data.save()


class UserAudioSerializer(serializers.ModelSerializer):
    """
    serialize UserAudio data
    """
    class Meta:
        model = UserAudio
        fields = "__all__"
        # fields = ('user', 'origin', 'audio_path', 'score')


class SearchSerializer(serializers.Serializer):
    """
    serialize search requests
    """
    id = serializers.IntegerField(allow_null=True)
