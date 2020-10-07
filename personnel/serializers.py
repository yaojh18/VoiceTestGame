"""
Serializers for personnel.
"""
# pylint: disable=E5142, W0223, W0221, R0201
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile


class ReadGroupInfo(serializers.RelatedField):
    """
    How to display Group informations.
    """
    def to_representation(self, obj):
        myout = list()
        for group in obj.all():
            myout.append({"id": group.pk, "name": group.name})
        return myout


class OpenIdInfo(serializers.RelatedField):
    def to_representation(self, obj):
        return obj.openid


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
            return User.objects.create_user(**validated_data, first_name=name)
        return User.objects.create_user(**validated_data)


class WechatLoginSerializer(serializers.Serializer):
    openid = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=128, required=False)
    password = serializers.CharField(max_length=128, required=False)

    def validate(self, attrs):
        res = dict()
        res['openid'] = attrs['openid']
        res['username'] = 'wx_' + attrs['openid']
        res['password'] = make_password(res['username'])
        return res

    def create(self, validated_data):
        open_id = validated_data.pop('openid')
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        userprofile = UserProfile(user=user, openid=open_id)
        userprofile.save()
        return user