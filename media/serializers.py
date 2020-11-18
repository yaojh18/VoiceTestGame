"""
Serializers for media app
"""
# pylint: disable=E5142, W0223, W0221, R0201, C0301
from django.db.models import Max, Avg, Q, F
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
            'type_id': {'required': False},
            'title': {'required': False},
            'content': {'required': False},
            'audio_path': {'required': False},
            'video_path': {'required': False},
        }

    def update(self, instance, validated_data):
        if 'type_id' in validated_data:
            type_id = validated_data.pop('type_id')
            if type_id != instance.type_id:
                previous_type_id = instance.type_id
                previous_level_id = instance.level_id
                instance.type_id = type_id
                instance.level_id = instance.generate_level_id
                instance.save()
                medias = OriginMedia.objects.filter(type_id=previous_type_id, level_id__gt=previous_level_id)
                medias.update(level_id=F('level_id') - 1)
        return super().update(instance, validated_data)


class MediaListSerializer(serializers.ModelSerializer):
    """
    serializer for list of origin media data
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id', 'type_id', 'title']


class LevelListSerializer(serializers.ListSerializer):
    """
    Serializer for media level id resorting.
    List Serializer.
    """
    def validate(self, attrs):
        medias = list()
        level_ids = list()
        for item in attrs:
            if 'id' not in item or 'level_id' not in item:
                raise serializers.ValidationError('Please input id and level_id')
            media = OriginMedia.objects.filter(id=item['id']).first()
            if media is None:
                raise serializers.ValidationError('Id does not exist.')
            medias.append(media)
            level_ids.append(item['level_id'])
        type_id = medias[0].type_id
        for media in medias:
            if media.level_id not in level_ids:
                raise serializers.ValidationError('Level ids are not consistent.')
            if media.type_id != type_id:
                raise serializers.ValidationError('The media must belong to the same type.')
        return attrs

    def create(self, validated_data):
        obj_lst = list()
        for item in validated_data:
            media = OriginMedia.objects.get(id=item['id'])
            media.level_id = item['level_id']
            obj_lst.append(media)
        OriginMedia.objects.bulk_update(obj_lst, fields=['level_id'])
        return obj_lst


class MediaResortSerializer(serializers.ModelSerializer):
    """
    Serializer for media level id resorting.
    """
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
    type_id = serializers.CharField(max_length=1)


class MediaAnalysisSerializer(serializers.ModelSerializer):
    """
    serializer for media data analysis
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'type_id', 'level_id', 'title']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        origin_media = OriginMedia.objects.get(pk=instance.id)
        users = origin_media.users.all()
        played_num = users.count()
        unknown = users.filter(user__userprofile__gender='0')
        male = users.filter(user__userprofile__gender='1')
        female = users.filter(user__userprofile__gender='2')
        data['played_num'] = played_num
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['score_average'] = users.aggregate(score=Avg('score'))['score']
        data['unknown_score_average'] = unknown.aggregate(score=Avg('score'))['score']
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
        user = User.objects.get(pk=instance.user.id)
        data['user'] = user.username
        data['level'] = user.audios.aggregate(level=Max('media__level_id'))['level']
        if data['level'] is None:
            data['level'] = 0
        else:
            data['level'] += 1
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
        type_id = OriginMedia.objects.get(id=instance.media.id).type_id
        data['type_id'] = type_id
        return data


class MediaChartSerializer(serializers.ModelSerializer):
    """
    serializer for media charts of one level
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'type_id', 'level_id', 'title']

    def to_representation(self, instance):
        data = dict()
        origin_media = OriginMedia.objects.get(pk=instance.id)
        users = origin_media.users.all()
        unknown = users.filter(user__userprofile__gender='0')
        male = users.filter(user__userprofile__gender='1')
        female = users.filter(user__userprofile__gender='2')
        scores = []
        unknown_scores = []
        male_scores = []
        female_scores = []
        for i in range(10):
            scores.append(users.filter(Q(score__gt=i * 10) & Q(score__lte=(i + 1) * 10)).count())
            unknown_scores.append(unknown.filter(Q(score__gt=i * 10)
                                                 & Q(score__lte=(i + 1) * 10)).count())
            male_scores.append(male.filter(Q(score__gt=i * 10)
                                           & Q(score__lte=(i + 1) * 10)).count())
            female_scores.append(female.filter(Q(score__gt=i * 10)
                                               & Q(score__lte=(i + 1) * 10)).count())
        data['level_id'] = instance.level_id
        data['type_id'] = instance.type_id
        data['title'] = instance.title
        data['played_num'] = users.count()
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['score_average'] = users.aggregate(score=Avg('score'))['score']
        data['unknown_score_average'] = unknown.aggregate(score=Avg('score'))['score']
        data['male_score_average'] = male.aggregate(score=Avg('score'))['score']
        data['female_score_average'] = female.aggregate(score=Avg('score'))['score']
        data['scores'] = scores
        data['unknown_scores'] = unknown_scores
        data['male_scores'] = male_scores
        data['female_scores'] = female_scores
        return data


class UserChartSerializer(serializers.ModelSerializer):
    """
    serializer for user charts
    """

    class Meta:
        model = UserProfile

    def to_representation(self, instance):
        users = UserProfile.objects.all()
        unknown = users.filter(gender="0")
        male = users.filter(gender='1')
        female = users.filter(gender='2')
        levels = []
        level_num = OriginMedia.objects.all().aggregate(level=Max('level_id'))['level']
        for _ in range(level_num+2):
            levels.append(0)
        for item in users:
            index = item.user.audios.aggregate(level=Max('media__level_id'))['level']
            if index is not None:
                levels[index+1] += 1
            else:
                levels[0] += 1
        data = dict()
        data['num'] = users.count()
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['level_count'] = levels
        return data


class UserAudioChartSerializer(serializers.ModelSerializer):
    """
    serializer for user audio charts
    """

    class Meta:
        model = UserAudio

    def to_representation(self, instance):
        audio = UserAudio.objects.all().order_by('timestamp')
        unknown = audio.filter(user__userprofile__gender="0")
        male = audio.filter(user__userprofile__gender='1')
        female = audio.filter(user__userprofile__gender='2')
        time_count = dict()
        time_format = '%Y-%m-%d'
        if not audio.count() == 0:
            time_count[audio[0].timestamp.date().strftime(time_format)] = 1
            last = 0
            for i in range(1, audio.count()):
                if audio[i].timestamp.date() == audio[i - 1].timestamp.date():
                    continue
                time_count[audio[i - 1].timestamp.date().strftime('%Y-%m-%d')] = i - last
                last = i
            i = audio.count()
            if i > 1 and \
                    audio[i - 1].timestamp.date() == audio[i - 2].timestamp.date():
                time_count[audio[i - 1].timestamp.date().strftime(time_format)] = i - last
            else:
                time_count[audio[i - 1].timestamp.date().strftime(time_format)] = 1
        data = dict()
        data['num'] = audio.count()
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['time_count'] = time_count
        return data
