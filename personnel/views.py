"""
Define API for frontend here.
"""
# pylint: disable=E5142, R0901, C0301, R0201
import requests
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Max
from config.local_settings import WEAPP_ID, WEAPP_SECRETE
from media.models import OriginMedia
from .models import UserAudio
from .serializers import UserInfoSerializer, UserLoginSerializer, \
    UserRegistrationSerializer, UserProfileSerializer, WechatLoginSerializer, \
    UserAudioSerializer, UserUpdateSerializer
# Create your views here.



def get_wechat_credential(code):
    """
    Get openid from backend of Wechat,
    using url:https://api.weixin.qq.com/sns/jscode2session.
    """
    login_response = requests.get('https://api.weixin.qq.com/sns/jscode2session', params={
        'appid': WEAPP_ID,
        'secret': WEAPP_SECRETE,
        'js_code': code,
        'grant_type': 'authorization_code'
    })
    login_response = login_response.json()
    return login_response


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """
    Define API under api/user/ .
    """
    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserInfoSerializer

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        if self.request.user.is_anonymous:
            return User.objects.none()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        API for api/user/login
        """

        res = self.get_serializer_class()(data=request.data)
        if res.is_valid():
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        """
        API for api/user/registration
        """
        res = self.get_serializer_class()(data=request.data)
        print(res)
        if res.is_valid():
            res.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if len(response.data) == 1:
            response.data = response.data[0]
        return response


class WechatViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
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

    @action(detail=False, methods=['POST'], authentication_classes = [])
    def login(self, request):
        """
        API for /api/wechat/login.
        """
        if 'code' in request.data:
            login_response = get_wechat_credential(request.data['code'])
        else:
            return Response({'msg': 'Please provide session_id'}, status=status.HTTP_404_NOT_FOUND)
        if 'errcode' in login_response:
            return Response({'msg': 'Wrong session_id'}, status=status.HTTP_404_NOT_FOUND)
        res = self.get_serializer_class()(data=login_response)
        if res.is_valid():
            return Response(res.data, status=status.HTTP_200_OK)
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
                res.save()
                return Response(res.data, status=status.HTTP_200_OK)
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
        if user.has_perm('auth.audio') and 'level_id' in params:
            length = params.get('length', default=5)
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
        if user.has_perm('auth.audio') and 'level_id' in params:
            media_id = OriginMedia.objects.filter(level_id=params.get('level_id')).first()
            if media_id is not None:
                user_id = params.get('user_id', default=user.id)
                user_audio = UserAudio.objects.filter(media_id=media_id, user_id=user_id).order_by('-score').first()
                if user_audio is not None:
                    return Response({'audio_url': user_audio.audio.url}, status=status.HTTP_200_OK)
        return Response({'msg': 'Please input the correct level_id'},status=status.HTTP_404_NOT_FOUND)
