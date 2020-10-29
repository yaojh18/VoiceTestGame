"""
Serializers for personnel.
"""
# pylint: disable=E5142, W0223, W0221, R0201
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from media.models import OriginMedia
from .models import UserProfile, UserAudio


class ReadGroupInfo(serializers.RelatedField):
    """
    How to display Group informations.
    """
    def to_representation(self, obj):
        myout = list()
        for group in obj.all():
            myout.append({"id": group.pk, "name": group.name})
        return myout


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Display user information for admin.
    """
    name = serializers.SerializerMethodField(read_only=True)
    groups = ReadGroupInfo(read_only=True)

    def get_name(self, obj):
        """
        Display user:name format.
        """
        return obj.first_name + obj.last_name

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'is_superuser',
                    'date_joined', 'last_login', 'groups']


class UserLoginSerializer(serializers.Serializer):
    """
    Determine the format of user data when logging in.
    """
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError
        self.instance = User.objects.get(username=attrs['username'])
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Determine the format of user data when registering.
    """
    name = serializers.CharField(max_length=128, required=False)
    password2 = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'password2']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError
        return attrs

    def create(self, validated_data):
        if 'name' in validated_data:
            name = validated_data.pop('name')
            user = User.objects.create_user(**validated_data, first_name=name)
        else:
            user = User.objects.create_user(**validated_data)
        visitor = Group.objects.get(name='visitor')
        user.groups.add(visitor)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Determine the format of userporfile data when updating.
    """
    nick_name = serializers.CharField(source='first_name')
    gender = serializers.CharField(source='userprofile.gender', write_only=True)
    city = serializers.CharField(source='userprofile.city', write_only=True)
    province = serializers.CharField(source='userprofile.province', write_only=True)
    avatar_url = serializers.CharField(source='userprofile.avatar_url')
    user_id = serializers.IntegerField(source='id',read_only=True)
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'nick_name', 'gender', 'city', 'province', 'avatar_url', 'score']

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        profile = instance.userprofile
        profile.gender = validated_data['userprofile']['gender']
        profile.city = validated_data['userprofile']['city']
        profile.province = validated_data['userprofile']['province']
        profile.avatar_url = validated_data['userprofile']['avatar_url']
        instance.save()
        profile.save()
        return instance


class UserAudioSerializer(serializers.ModelSerializer):
    """
    Determine the format of user audio data when writing.
    """
    level_id = serializers.IntegerField()

    class Meta:
        model = UserAudio
        fields = ['audio', 'level_id']

    def create(self, validated_data):
        user = self.context['user']
        media = OriginMedia.objects.get(level_id=validated_data['level_id'])
        user_audio = UserAudio(user=user, media=media)
        user_audio.audio.save(content=validated_data['audio'], name=user_audio.get_audio_name())
        user_audio.save()
        return user_audio


class WechatLoginSerializer(serializers.Serializer):
    """
    Login designed for wechat
    """
    openid = serializers.CharField(required=True, source='userprofile.openid')
    username = serializers.CharField(max_length=128, required=False, read_only=True)
    password = serializers.CharField(max_length=128, required=False, read_only=True)

    def validate(self, attrs):
        res = dict()
        res['openid'] = attrs['userprofile']['openid']
        res['username'] = 'wx_' + attrs['userprofile']['openid']
        res['password'] = make_password(res['username'])
        self.instance = User.objects.filter(username=res['username']).first()
        return res

    def create(self, validated_data):
        open_id = validated_data.pop('openid')
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
        userprofile = UserProfile(user=user, openid=open_id)
        userprofile.save()
        visitor = Group.objects.get(name='visitor')
        user.groups.add(visitor)
        return user

    def update(self, instance, validated_data):
        return instance
