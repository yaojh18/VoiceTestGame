"""
Serializers for personnel.
"""
# pylint: disable=E5142, W0223, W0221, R0201
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
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
        fields = ['id', 'username', 'password', 'name', 'email', 'is_superuser', 'is_staff',
                  'is_active', 'date_joined', 'last_login', 'groups']


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


class UserProfileSerializer(serializers.Serializer):
    """
    Determine the format of userporfile data when updating.
    """
    nick_name = serializers.CharField(source='first_name')
    gender = serializers.CharField(source='userprofile.gender')
    city = serializers.CharField(source='userprofile.city')
    province = serializers.CharField(source='userprofile.province')

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        profile = instance.userprofile
        profile.gender = validated_data['userprofile']['gender']
        profile.city = validated_data['userprofile']['city']
        profile.province = validated_data['userprofile']['province']
        instance.save()
        profile.save()
        return instance


class UserAudioSerializer(serializers.ModelSerializer):
    """
    Determine the format of user audio data when writing.
    """
    class Meta:
        model = UserAudio
        fields = ['audio', 'media']

    def create(self, validated_data):
        user = self.context['user']
        user_audio = UserAudio(user=user, media=validated_data['media'])
        user_audio.audio.save(
            name=user_audio.get_audio_name(), content=validated_data['audio'])
        user_audio.save()
        return user_audio


class WechatLoginSerializer(serializers.Serializer):
    """
    Login designed for wechat
    """
    openid = serializers.CharField(required=True, source='userprofile.openid')
    username = serializers.CharField(max_length=128, required=False)
    password = serializers.CharField(max_length=128, required=False)

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
