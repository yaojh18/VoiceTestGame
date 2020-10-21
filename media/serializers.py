"""
Serializers for media app
"""
# pylint: disable=E5142, W0223, W0221, R0201
from rest_framework import serializers
from .models import OriginMedia
from personnel.models import UserAudio


class OriginMediaSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """
    class Meta:
        model = OriginMedia
        fields = "__all__"
        read_only_fields = ['media_id']

    # def validate(self, attrs):
    #     if not attrs['media_id']:
    #         attrs['media_id'] = self.media_id_default()
    #     super(OriginMediaSerializer, self).validate()

    def create(self, validated_data):
        validated_data['media_id'] = self.media_id_default()
        # print(validated_data)
        # media_obj = OriginMedia.objects.create(validated_data)
        return super(OriginMediaSerializer, self).create(validated_data)

    def media_id_default(self):
        """
        return default value of media_id
        """
        if OriginMedia.objects.count() == 0:
            print('count=0')
            return 0
        media_id_list = OriginMedia.objects.order_by('media_id').values_list('media_id')
        print('media_id_list:',media_id_list)
        num = 0
        while True:
            if OriginMedia.objects.count() == num:
                return num
            if media_id_list[num][0] != num:
                print('break num:',media_id_list[num][0])
                break
            num += 1
        return num+1


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

    def update_data(self):
        """
        update data
        """
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


class ListOriginSerializer(serializers.ModelSerializer):
    """
    serializer for list of origin media data
    """
    class Meta:
        model = OriginMedia
        fields = ['id', 'title']


class UserAudioListSerializer(serializers.ModelSerializer):
    """
    serializer for list of user audio
    """
    class Meta:
        model = UserAudio
        fields = ['timestamp', 'score']
