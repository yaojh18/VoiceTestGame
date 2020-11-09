"""
Serializers for media app
"""
# pylint: disable=E5142, W0223, W0221, R0201\
from django.db.models import Max, Avg, Q
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
        # extra_kwargs = {
        #     'level_id': {'allow_null': True},
        # }

    def create(self, validated_data):
        # if not validated_data['level_id']:
        #     validated_data['level_id'] = self.level_id_default()
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
        exclude = ['speaker_id', 'level_id']
        extra_kwargs = {
            # 'level_id': {'allow_null': True, ''},
            'title': {'allow_null': True},
            'content': {'allow_null': True},
            'audio_path': {'allow_null': True},
            'video_path': {'allow_null': True},
        }

    def update(self, instance, validated_data):
        # if validated_data['level_id']:
        #     instance.title = validated_data['level_id']
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
        # passed_users = users.filter(score__gt=60)
        played_num = users.count()
        # passed_num = passed_users.count()
        # passed_proportion = None
        # if not played_num == 0:
        #     passed_proportion = passed_num / played_num
        unknown = users.filter(user__userprofile__gender='0')
        male = users.filter(user__userprofile__gender='1')
        female = users.filter(user__userprofile__gender='2')
        data['played_num'] = played_num
        # data['passed_num'] = passed_num
        # data['passed_proportion'] = passed_proportion
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        # data['passed_unknown_gender'] = passed_users.filter(user__userprofile__gender='0').count()
        # data['passed_male'] = passed_users.filter(user__userprofile__gender='1').count()
        # data['passed_female'] = passed_users.filter(user__userprofile__gender='2').count()
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


class MediaChartSerializer(serializers.ModelSerializer):
    """
    serializer for media charts of one level
    """

    class Meta:
        model = OriginMedia
        fields = ['id', 'level_id', 'title']

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
            score = users.filter(Q(score__gt=i * 10) & Q(score__lte=(i + 1) * 10)).count()
            unknown_score = unknown.filter(Q(score__gt=i * 10) & Q(score__lte=(i + 1) * 10)).count()
            male_score = male.filter(Q(score__gt=i * 10) & Q(score__lte=(i + 1) * 10)).count()
            female_score = female.filter(Q(score__gt=i * 10) & Q(score__lte=(i + 1) * 10)).count()
            scores.append(score)
            unknown_scores.append(unknown_score)
            male_scores.append(male_score)
            female_scores.append(female_score)
        data['level_id'] = instance.level_id
        data['title'] = instance.title
        data['played_num'] = users.count()
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['score_average'] = users.aggregate(score=Avg('score'))['score']
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
        level_num = OriginMedia.objects.all().count()
        for i in range(level_num):
            levels.append(0)
            # level = users.filter(users.aggregate(level=Max('user__audios__media__level_id'))['level'] == i).count()
        for item in users:
            index = item.user.audios.aggregate(level=Max('media__level_id'))['level']
            if index is not None:
                levels[index] += 1
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
        time_count[audio[0].timestamp.date().strftime('%Y-%m-%d')] = 1
        last = 0
        for i in range(1, audio.count()):
            if audio[i].timestamp.date() == audio[i - 1].timestamp.date():
                continue
            time_count[audio[i - 1].timestamp.date().strftime('%Y-%m-%d')] = i - last
            last = i
        i = audio.count()
        if i > 1 and \
                audio[i - 1].timestamp.date() == audio[i - 2].timestamp.date():
            time_count[audio[i - 1].timestamp.date().strftime('%Y-%m-%d')] += 1
        else:
            time_count[audio[i - 1].timestamp.date().strftime('%Y-%m-%d')] = 1
        data = dict()
        data['num'] = audio.count()
        data['unknown_num'] = unknown.count()
        data['male_num'] = male.count()
        data['female_num'] = female.count()
        data['time_count'] = time_count
        return data
# class MediaChartSerializer(serializers.ModelSerializer):
#     """
#     serializer for media charts
#     """
#     class Meta:
#         model = OriginMedia
#         fields =
