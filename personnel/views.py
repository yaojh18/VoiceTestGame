"""
Define API for frontend here.
"""
# pylint: disable=E5142, R0901
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserInfoSerializer, UserLoginSerializer, UserRegistrationSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    Define API under api/user/ .
    """
    #queryset = User.objects.all()
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
            return Response({'code':status.HTTP_200_OK, 'token': ''})
        return Response({'code':status.HTTP_401_UNAUTHORIZED, 'msg': res.errors})

    @action(detail=False, methods=['POST'])
    def registration(self, request):
        """
        API for api/user/registration
        """
        self.serializer_class = UserRegistrationSerializer
        res = self.serializer_class(data=request.data)
        if res.is_valid():
            res.save()
            return Response({'code':status.HTTP_200_OK, 'token': ''})
        return Response({'code':status.HTTP_401_UNAUTHORIZED, 'msg': res.errors})
