"""
Serializers for media app
"""
# pylint: disable=E5142, W0223, W0221, R0201\
from django.db.models import Q, Avg
from rest_framework import serializers
from personnel.models import UserAudio, UserProfile
from .models import OriginMedia


class MediaCreateSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """

    class Meta:
        model = OriginMedia
        fields = "__all__"
        extra_kwargs = {
            'level_id': {'allow_null': True},
        }

    def create(self, validated_data):
        if not validated_data['level_id']:
            validated_data['level_id'] = self.level_id_default()
        return super().create(validated_data)

    def level_id_default(self):
        """
        return default value of level_id
        """
        if OriginMedia.objects.count() == 0:
            return 0
        level_id_list = OriginMedia.objects.order_by('level_id').values_list('level_id')
        num = 0
        while OriginMedia.objects.count() > num and level_id_list[num][0] == num:
            num += 1
        return num


class MediaUpdateSerializer(serializers.ModelSerializer):
    """
    serialize OriginMedia data
    """

    class Meta:
        model = OriginMedia
        fields = "__all__"
        # read_only_fields = ['level_id']
        extra_kwargs = {
            'level_id': {'allow_null': True},
            'title': {'allow_null': True},
            'content': {'allow_null': True},
            'audio_path': {'allow_null': True},
            'video_path': {'allow_null': True},
        }

    def update(self, instance, validated_data):
        if validated_data['level_id']:
            instance.title = validated_data['level_id']
        if validated_data['title']:
            instance.title = validated_data['title']
        if validated_data['content']:
            instance.content = validated_data['content']
        if validated_data['audio_path']:
            instance.audio_path = validated_data['audio_path']
        if validated_data['video_path']:
            instance.video_path = validated_data['video_path']
        instance.save()
        return instance


class MediaListSerializer(serializers.ModelSerializer):
    """
    serializer for list of origin media data
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id', 'title']


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
        # print(users.values())
        passed_users = users.filter(score__gt=0)
        played_num = users.count()
        passed_num = passed_users.count()
        passed_proportion = None
        if not played_num == 0:
            passed_proportion = passed_num / played_num
        male = users.filter(user__userprofile__gender='0')
        female = users.filter(user__userprofile__gender='1')
        passed_male = passed_users.filter(user__userprofile__gender='0')
        passed_female = passed_users.filter(user__userprofile__gender='1')
        score_average = passed_users.aggregate(score=Avg('score'))['score']
        male_score_average = passed_male.aggregate(score=Avg('score'))['score']
        female_score_average = passed_female.aggregate(score=Avg('score'))['score']
        data['played_num'] = played_num
        data['passed_num'] = passed_num
        data['passed_proportion'] = passed_proportion
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['passed_male'] = passed_male.count()
        data['passed_female'] = passed_female.count()
        data['score_average'] = score_average
        data['male_score_average'] = male_score_average
        data['female_score_average'] = female_score_average
        return data


class UserAnalysisSerializer(serializers.ModelSerializer):
    """
    serializer for user data analysis
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'level']


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
        level = OriginMedia.objects.get(id=instance.media.id).level_id
        data['level_id'] = level
        return data
