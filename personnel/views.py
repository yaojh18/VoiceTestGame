"""
Define API for frontend here.
"""
# pylint: disable=E5142, R0901, C0301, R0201, R0903
import requests
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Max
from config.local_settings import WEAPP_ID, WEAPP_SECRETE
from media.models import OriginMedia
from .models import UserAudio, AudioPermission, ProfilePermission
from .serializers import UserLoginSerializer, \
    UserRegistrationSerializer, UserProfileSerializer, WechatLoginSerializer, \
    UserAudioSerializer, UserUpdateSerializer, UserListSerializer
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


class ListModelMixin:
    """
    Create a model instance.
    """
    def list(self, request):
        """
        Mixin list method.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if len(queryset) == 1:
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  ListModelMixin):
    """
    Define API under api/user/ .
    """

    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserUpdateSerializer

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        if self.request.user.has_perm('auth.management'):
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAuthenticated(),]
        return []

    def put(self, request):
        """
        API for api/user/registration
        """
        if self.request.path_info != '/api/users/':
            return Response(status=status.HTTP_404_NOT_FOUND)
        res = self.get_serializer(data=request.data)
        if res.is_valid():
            res.save()
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        API for api/user/login
        """
        res = self.get_serializer(data=request.data)
        if res.is_valid():
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_403_FORBIDDEN)


class WechatViewSet(viewsets.GenericViewSet,
                    ListModelMixin):
    """
    Define API for /api/wechat/.
    """

    def get_serializer_class(self):
        """
        Get serializer class automatically.
        """
        if self.action == 'audio':
            return UserAudioSerializer
        if self.action == 'login':
            return WechatLoginSerializer
        return UserProfileSerializer

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        if self.request.user.has_perm('auth.profile'):
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [ProfilePermission()]
        if self.action == 'list' or self.action == 'login':
            return [IsAuthenticated()]
        return []

    def create(self, request):
        """
        API for /api/wechat/profile.
        """
        user = request.user
        res = self.get_serializer(instance=user, data=request.data)
        if res.is_valid():
            res.save()
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        API for /api/wechat/login.
        """
        if 'code' in request.data:
            login_response = get_wechat_credential(request.data['code'])
        else:
            return Response({'msg': 'Please provide session_id'}, status=status.HTTP_400_BAD_REQUEST)
        if 'errcode' in login_response:
            return Response({'msg': 'Wrong session_id'}, status=status.HTTP_404_NOT_FOUND)
        res = self.get_serializer(data=login_response)
        if res.is_valid():
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, AudioPermission])
    def audio(self, request):
        """
        API for /api/wechat/audio.
        """
        user = request.user
        res = self.get_serializer(data=request.data, context={'user': user})
        if res.is_valid():
            res.save()
            return Response(res.data, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_400_BAD_REQUEST)


class LevelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Define API for /api/level/.
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, AudioPermission]
    http_method_names = ['get']

    def get_queryset(self):
        """
        Get queryset automatically.
        """
        params = self.request.query_params
        if 'level_id' in params:
            length = params.get('length', default=5)
            level_id = params.get('level_id')
            type_id = params.get('type_id', default='0')
            media_id = OriginMedia.objects.filter(level_id=level_id, type_id=type_id).first()
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
        user = request.user
        params = request.query_params
        if 'level_id' in params:
            level_id = params.get('level_id')
            type_id = params.get('type_id', default='0')
            media_id = OriginMedia.objects.filter(level_id=level_id, type_id=type_id).first()
            if media_id is not None:
                user_id = params.get('user_id', default=user.id)
                user_audio = UserAudio.objects.filter(media_id=media_id, user_id=user_id).order_by('-score').first()
                if user_audio is not None:
                    return Response({
                        'audio_url': request.build_absolute_uri(user_audio.audio.url)},
                        status=status.HTTP_200_OK)
        return Response({'msg': 'Please input the correct level_id'}, status=status.HTTP_404_NOT_FOUND)
