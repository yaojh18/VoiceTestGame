"""
Define API for frontend here.
"""
# pylint: disable=E5142, R0901, C0301, R0201
import requests
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.db.models import Max
from config.local_settings import WEAPP_URL, WEAPP_ID, WEAPP_SECRETE, APP_URL, APP_ID, APP_SECRET
from media.models import OriginMedia
from .models import UserAudio
from .serializers import UserInfoSerializer, UserLoginSerializer, \
    UserRegistrationSerializer, UserProfileSerializer, WechatLoginSerializer, \
    UserAudioSerializer
# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def get_wechat_credential(code):
    """
    Get openid from backend of Wechat,
    using url:https://api.weixin.qq.com/sns/jscode2session.
    """
    login_response = requests.get(WEAPP_URL, params={
        'appid': WEAPP_ID,
        'secret': WEAPP_SECRETE,
        'js_code': code,
        'grant_type': 'authorization_code'
    })
    login_response = login_response.json()
    return login_response


def get_audio_credential():
    """
    Get score from audio backend.
    """
    response = requests.post(APP_URL + '/interface/auxiliary/getSpeakerId', json={
        "id_type": "1",
        "id_number": "130982200005248419",
        "app_id": APP_ID,
        "secret": APP_SECRET
    })
    speaker_id = response.json()['speakerId']
    response = requests.post(APP_URL + '/interface/text/training/get', json={
        'speaker_id': speaker_id,
        'text_type': "4113",
        'app_id': APP_ID,
        'secret': APP_SECRET
    })
    session_id = response.json()['session_id']
    print(session_id)


def get_user_token(user):
    """
    JWT default way to get user token.
    """
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return jwt_response_payload_handler(token, user)


class UserViewSet(viewsets.ModelViewSet):
    """
    Define API under api/user/ .
    """
    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'registration':
            return  UserRegistrationSerializer
        return UserInfoSerializer

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.none()

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        API for api/user/login
        """

        res = self.get_serializer_class()(data=request.data)
        if res.is_valid():
            token = get_user_token(res.instance)
            return Response(token, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'])
    def registration(self, request):
        """
        API for api/user/registration
        """
        res = self.get_serializer_class()(data=request.data)
        if res.is_valid():
            user = res.save()
            return Response(get_user_token(user), status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_401_UNAUTHORIZED)


class WechatViewSet(viewsets.ModelViewSet):
    """
    Define API for /api/wechat/.
    """
    def get_serializer_class(self):
        """
        Get serializer class automatically.
        """
        if self.action == 'profile':
            return UserProfileSerializer
        if self.action == 'audio':
            return UserAudioSerializer
        return WechatLoginSerializer
    def get_queryset(self):
        """
        Get queryset automatically.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.none()


    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        API for /api/wechat/login.
        """
        login_response = get_wechat_credential(request.data['code'])
        if 'errcode' in login_response:
            return Response({'msg': 'Wrong session_id'}, status=status.HTTP_404_NOT_FOUND)
        res = self.get_serializer_class()(data=login_response)
        if res.is_valid():
            user = res.save()
            return Response(get_user_token(user), status=status.HTTP_200_OK)
        return Response({'msg':res.errors}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, ] )
    def profile(self, request):
        """
        API for /api/wechat/profile.
        """
        user = request.user
        if user.has_perm('auth.profile'):
            res = self.get_serializer_class()(instance=user, data=request.data)
            if res.is_valid():
                res.save()
                level = user.audios.aggregate(level=Max('media__level_id'))
                if level['level'] is None:
                    level['level'] = 0
                return Response(level, status=status.HTTP_200_OK)
            return Response({'msg': res.errors}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg': 'Manager has no profile'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, ])
    def audio(self, request):
        """
        API for /api/wechat/audio.
        """
        user = request.user
        if user.has_perm('auth.audio'):
            res = self.get_serializer_class()(data=request.data, context={'user': user})
            if res.is_valid():
                user_audio = res.save()
                return Response({'score': user_audio.score}, status=status.HTTP_200_OK)
            return Response({'msg': res.errors}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg': 'Manager has no audio'}, status=status.HTTP_403_FORBIDDEN)


class LevelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Define API for /api/level/.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get']

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        user = self.request.user
        params = self.request.query_params
        if user.has_perm('auth.audio'):
            length = params.get('length', default=5)
            if 'level_id' in params:
                media_id = OriginMedia.objects.filter(level_id=params.get('level_id')).first()
                if media_id is not None:
                    users = User.objects.filter(audios__media=media_id).annotate(score=Max('audios__score'))
                    if users is not None:
                        return users.order_by('score')[:length]
        return User.objects.none()

    @action(detail=False, methods=['GET'])
    def audio(self, request):
        """
        API for /api/level/audio
        """
        user = self.request.user
        params = self.request.query_params
        if user.has_perm('auth.audio'):
            if 'level_id' in params:
                media_id = OriginMedia.objects.filter(level_id=params.get('level_id')).first()
                if media_id is not None:
                    user_id = params.get('user_id', default=user.id)
                    user_audio = UserAudio.objects.filter(media_id=media_id, user_id=user_id).order_by('-score').first()
                    if user_audio is not None:
                        return Response({'audio_url': user_audio.audio.url}, status=status.HTTP_200_OK)
        return Response({'msg': 'Please input the correct level_id'},status=status.HTTP_404_NOT_FOUND)
