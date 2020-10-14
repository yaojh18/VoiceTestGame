"""
Define API for frontend here.
"""
# pylint: disable=E5142, R0901
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from config.local_settings import WEAPP_ID, WEAPP_SECRETE
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
    auth_url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = dict()
    params['appid'] = WEAPP_ID
    params['secret'] = WEAPP_SECRETE
    params['js_code'] = code
    params['grant_type'] = 'authorization_code'
    login_response = requests.get(auth_url, params=params)
    login_response = login_response.json()
    return login_response


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
    queryset = User.objects.none()
    serializer_class = UserInfoSerializer

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
        self.serializer_class = UserLoginSerializer
        res = UserLoginSerializer(data=request.data)
        if res.is_valid():
            token = get_user_token(res.instance)
            return Response(token, status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'])
    def registration(self, request):
        """
        API for api/user/registration
        """
        self.serializer_class = UserRegistrationSerializer
        res = self.serializer_class(data=request.data)
        if res.is_valid():
            user = res.save()
            return Response(get_user_token(user), status=status.HTTP_200_OK)
        return Response({'msg': res.errors}, status=status.HTTP_401_UNAUTHORIZED)


class WechatViewSet(viewsets.ModelViewSet):
    """
    Define API for /api/wechat/.
    """
    queryset = User.objects.none()
    serializer_class = WechatLoginSerializer

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
        res = self.serializer_class(data=login_response)
        if res.is_valid():
            user = res.save()
            return Response(get_user_token(user), status=status.HTTP_200_OK)
        return Response({'msg':res.errors}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, ])
    def profile(self, request):
        """
        API for /api/wechat/profile.
        """
        user = request.user
        if user.has_perm('auth.profile'):
            self.serializer_class = UserProfileSerializer
            res = self.serializer_class(instance=user, data=request.data)
            if res.is_valid():
                res.save()
                return Response({'level': user.userprofile.level}, status=status.HTTP_200_OK)
            return Response({'msg': res.errors}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg': 'Manager has no profile'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, ])
    def audio(self, request):
        """
        API for /api/wechat/audio.
        """
        user = request.user
        if user.has_perm('auth.audio'):
            self.serializer_class = UserAudioSerializer
            res = self.serializer_class(data=request.data, context={'user': user})
            if res.is_valid():
                user_audio = res.save()
                return Response({'score': user_audio.score}, status=status.HTTP_200_OK)
            return Response({'msg': res.errors}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg': 'Manager has no audio'}, status=status.HTTP_403_FORBIDDEN)
