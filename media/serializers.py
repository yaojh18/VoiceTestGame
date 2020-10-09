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


class SearchOriginSerializer(serializers.Serializer):
    """
        serialize search requests
        """
    id = serializers.IntegerField(allow_null=True)


class EditOriginSerializer(serializers.Serializer):
    """
    serialize edit requests
    """
    id = serializers.IntegerField(allow_null=True)
    title = serializers.CharField(max_length=64, allow_null=True)
    content = serializers.CharField(max_length=1024, allow_null=True)
    audio_path = serializers.FileField(max_length=256, allow_null=True)
    video_path = serializers.FileField(max_length=256, allow_null=True)

    def update_db(self):
        if not self.data['id']:
            return False
        try:
            data = OriginMedia.objects.get(pk=self.data['id'])
        except OriginMedia.DoesNotExist:
            return False
        if self.data['title']:
            data.title = self.data['title']
        if self.data['content']:
            data.content = self.data['content']
        if self.data['audio_path']:
            data.audio_path = self.data['audio_path']
        if self.data['video_path']:
            data.video_path = self.data['video_path']
        data.save()
        return True
