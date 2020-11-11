"""
Serializers for personnel.
"""
# pylint: disable=E5142, W0223, W0221, R0201, C0301
import datetime
import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from media.models import OriginMedia
from config.local_settings import APP_URL, APP_ID, APP_SECRET
from .models import UserProfile, UserAudio


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def get_speaker_id(audio_id, audio_path):
    """
    Create speaker id from audio backend.
    """
    response = requests.post(APP_URL + '/interface/auxiliary/getSpeakerId', json={
        "id_type": "0",
        "id_number": 'Dijkstra_' + str(audio_id),
        "app_id": APP_ID,
        "secret": APP_SECRET
    }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    speaker_id = response['speakerId']
    response = requests.post(APP_URL + '/interface/text/training/get', json={
        'speaker_id': speaker_id,
        'text_type': "4113",
        'app_id': APP_ID,
        'secret': APP_SECRET
    }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    session_id = response['session_id']
    response = requests.post(APP_URL + '/interface/voice/training/upload', files={
        'audio': ('audio', audio_path.open('rb'), 'audio/x-wav'),
        'json': (None, str({
            'session_id': session_id,
            'voice_index': '1',
            'bm_bits': 2,
            'bm_dt': 2
        }))
    }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    response = requests.post(APP_URL + '/interface/voiceprint/training/create', json={
            'session_id': session_id
        }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    return speaker_id


def get_audio_score(speaker_id, audio):
    """
    Get user audio score.
    """
    response = requests.post(APP_URL + '/interface/text/verification/get', json={
        'text_type': '8193',
        'speaker_id': speaker_id,
        'bm_bits': 2,
        'app_id': APP_ID,
        'secret': APP_SECRET
    }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    session_id = response['session_id']
    response = requests.post(APP_URL + '/interface/verification/score', files={
        'audio': ('audio', audio.open('rb'), 'audio/x-wav'),
        'json': (None, str({
            'session_id': session_id,
            'bm_bits': 2,
            'bm_dt': 2
        }))
    }).json()
    if 'errcode' in response and response['errcode'] != 0:
        raise serializers.ValidationError(response['errmsg'])
    return response['score']


def get_user_token(user):
    """
    JWT default way to get user token.
    """
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return jwt_response_payload_handler(token, user)['token']


class ReadGroupInfo(serializers.RelatedField):
    """
    How to display Group informations.
    """
    def to_representation(self, obj):
        group = obj.first()
        if hasattr(obj, 'pk'):
            return {"id": group.pk, "name": group.name}
        return {"id": None, "name": None}


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Display user information for admin.
    """
    groups = ReadGroupInfo(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'is_superuser',
                    'date_joined', 'last_login', 'groups']
        extra_kwargs = {
            'name': {'source': 'first_name'},
        }


class UserLoginSerializer(serializers.Serializer):
    """
    Determine the format of user data when logging in.
    """
    username = serializers.CharField(max_length=150, required=True, write_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """
        Automatically generate token.
        """
        return get_user_token(obj)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Please input the correct username and password.')
        self.instance = User.objects.get(username=attrs['username'])
        self.instance.last_login = datetime.datetime.now()
        self.instance.save()
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Determine the format of user data when registering.
    """
    name = serializers.CharField(source='first_name', write_only=True, required=False)
    password_confirm = serializers.CharField(max_length=128, required=True, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """
        Automatically generate token.
        """
        return get_user_token(obj)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'password_confirm', 'token']
        extra_kwargs = {
            'email': {'write_only': True, 'required': False},
            'password': {'write_only': True},
            'username': {'write_only': True, 'required': False}
        }

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('The passwords are not consistent.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        manager = Group.objects.get(name='manager')
        user.groups.add(manager)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Determine the format of user data when registering.
    """
    name = serializers.CharField(source='first_name', write_only=True, required=False)
    password_old = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'password_old']
        extra_kwargs = {
            'email': {'write_only': True, 'required': 'False'},
            'password': {'write_only': True},
            'username': {'write_only': True, 'required': False, 'validators': []}
        }

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).first()
        if user is None:
            raise serializers.ValidationError('Please input the correct username.')
        password_old = attrs.pop('password_old')
        if not user.check_password(password_old):
            raise serializers.ValidationError('Please input the correct password.')
        attrs['password'] = make_password(attrs['password'])
        self.instance = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Determine the format of userporfile data when updating.
    """
    nick_name = serializers.CharField(source='first_name')
    gender = serializers.CharField(source='userprofile.gender', write_only=True)
    city = serializers.CharField(source='userprofile.city', write_only=True)
    province = serializers.CharField(source='userprofile.province', write_only=True)
    avatar_url = serializers.CharField(source='userprofile.avatar_url')
    user_id = serializers.IntegerField(source='id', read_only=True)
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
    level_id = serializers.IntegerField(write_only=True)
    type_id = serializers.CharField(write_only=True, default='0')

    class Meta:
        model = UserAudio
        fields = ['level_id', 'audio', 'score', 'type_id']
        extra_kwargs = {
            'audio': {'write_only': True},
            'score': {'read_only': True}
        }

    def validate(self, attrs):
        media = OriginMedia.objects.filter(level_id=attrs['level_id'], type_id=attrs['type_id']).first()
        if media is None:
            raise serializers.ValidationError('Level id does not exist.')
        if media.speaker_id is None:
            media.speaker_id = get_speaker_id(media.id, media.audio_path)
        attrs['score'] = get_audio_score(media.speaker_id, attrs['audio'])
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        media = OriginMedia.objects.get(level_id=validated_data['level_id'])
        user_audio = UserAudio(user=user, media=media, score=validated_data['score'])
        user_audio.audio.save(content=validated_data['audio'], name=user_audio.get_audio_name)
        user_audio.save()
        return user_audio


class WechatLoginSerializer(serializers.Serializer):
    """
    Login designed for wechat
    """
    openid = serializers.CharField(source='userprofile.openid',write_only=True)
    username = serializers.HiddenField(
        default=serializers.CharField(max_length=128, read_only=True))
    password = serializers.HiddenField(
        default=serializers.CharField(max_length=128, read_only=True))
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """
        Automatically generate token.
        """
        return get_user_token(obj)

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
