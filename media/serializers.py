"""
Serializers for media app
"""
# pylint: disable=E5142, W0223, W0221, R0201\
from django.db.models import Avg
from django.contrib.auth.models import User
from rest_framework import serializers
from personnel.models import UserAudio, UserProfile
from .models import OriginMedia


class MediaCreateSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """

    class Meta:
        model = OriginMedia
        exclude = ['speaker_id', 'level_id']

    def create(self, validated_data):
        media = OriginMedia(**validated_data)
        media.level_id = media.generate_level_id
        media.save()
        return media


class MediaUpdateSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """

    class Meta:
        model = OriginMedia
        exclude = ['speaker_id', 'level_id']
        extra_kwargs = {
            'title': {'required': False},
            'content': {'required': False},
            'audio_path': {'required': False},
            'video_path': {'required': False},
        }


class MediaListSerializer(serializers.ModelSerializer):
    """
    serializer for list of origin media data
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id', 'title']


class LevelListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        medias = list()
        level_ids = list()
        for item in attrs:
            if 'id' not in item or 'level_id' not in item:
                raise serializers.ValidationError
            media = OriginMedia.objects.filter(id=item['id']).first()
            if media is None:
                raise serializers.ValidationError
            medias.append(media)
            level_ids.append(item['level_id'])
        for media in medias:
            if media.level_id not in level_ids:
                raise serializers.ValidationError
        return attrs

    def to_internal_value(self, data):
        obj_lst = list()
        for item in data:
            media = OriginMedia.objects.get(id=item['id'])
            media.level_id = item['level_id']
            obj_lst.append(media)
        OriginMedia.objects.bulk_update(obj_lst, fields=['level_id'])
        return obj_lst



class MediaResortSerializer(serializers.ModelSerializer):

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id']
        extra_kwargs = {
            'id': {'write_only': True, 'read_only': False},
            'level_id': {'write_only': True}
        }
        list_serializer_class = LevelListSerializer


class MediaSearchSerializer(serializers.Serializer):
    """
    serialize search requests
    """
    level_id = serializers.IntegerField(allow_null=True)


class MediaAnalysisSerializer(serializers.ModelSerializer):
    """
    serializer for media data analysis
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id', 'title']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        origin_media = OriginMedia.objects.get(pk=instance.id)
        users = origin_media.users.all()
        passed_users = users.filter(score__gt=60)
        played_num = users.count()
        passed_num = passed_users.count()
        passed_proportion = None
        if not played_num == 0:
            passed_proportion = passed_num / played_num
        male = users.filter(user__userprofile__gender='0')
        female = users.filter(user__userprofile__gender='1')
        data['played_num'] = played_num
        data['passed_num'] = passed_num
        data['passed_proportion'] = passed_proportion
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['passed_male'] = passed_users.filter(user__userprofile__gender='0').count()
        data['passed_female'] = passed_users.filter(user__userprofile__gender='1').count()
        data['score_average'] = users.aggregate(score=Avg('score'))['score']
        data['male_score_average'] = male.aggregate(score=Avg('score'))['score']
        data['female_score_average'] = female.aggregate(score=Avg('score'))['score']
        return data


class UserAnalysisSerializer(serializers.ModelSerializer):
    """
    serializer for user data analysis
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'gender']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = User.objects.get(pk=instance.user.id).username
        return data


class UserAudioAnalysisSerializer(serializers.ModelSerializer):
    """
    serializer for user audio data analysis
    """

    class Meta:
        model = UserAudio
        fields = ['user', 'media', 'audio', 'timestamp', 'score']
        extra_kwargs = {
            'media': {'write_only': True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = User.objects.get(pk=instance.user.id).username
        level = OriginMedia.objects.get(id=instance.media.id).level_id
        data['level_id'] = level
        return data
