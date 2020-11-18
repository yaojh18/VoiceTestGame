"""
Unity test for personnel.
"""
# pylint: disable=E5142, W0603, R0201
import json
import os
from django.test import TestCase
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from media.models import OriginMedia
from .serializers import WechatLoginSerializer
from .models import UserProfile, UserAudio

DELETE_FILES = []

class LogTest(TestCase):
    """
    Unity test for Login and Registration.
    """
    def setUp(self):
        user = ContentType.objects.get(model='user', app_label='auth')

        add_media = Permission.objects.create(
            content_type=user, codename='add_media', name="Can add new media")
        update_media = Permission.objects.create(
            content_type=user, codename='update_media',name='Can update existing media')
        query_media = Permission.objects.create(
            content_type=user, codename='query_media', name='Can query existing media')
        profile = Permission.objects.create(
            content_type=user, codename='profile', name='Have user profile')

        manager = Group.objects.create(name='manager')
        manager.permissions.add(add_media)
        manager.permissions.add(query_media)
        manager.permissions.add(update_media)
        manager.save()

        visitor = Group.objects.create(name='visitor')
        visitor.permissions.add(query_media)
        visitor.permissions.add(profile)
        visitor.save()

    def login(self, username=None, password=None):
        """
        Login method.
        """
        data = {
            'username': username,
            'password': password
        }
        return self.client.post('/api/users/login/', data=data)

    def registration(self, username=None, password=None, password2=None, name=None):
        """
        Registration method.
        """
        data = {
            'username': username,
            'password': password,
            'password_confirm': password2
        }
        if name:
            data['name'] = name
        return self.client.post('/api/users/', data=data)

    def login_for_wechat(self, session_id=None):
        """
        Login method for wechat.
        """
        data = {
            "code": session_id
        }
        return self.client.post('/api/wechat/login/', data=data)

    def test_registration(self):
        """
        Try to create test account.
        """
        response = self.registration('test', '123456', '123456')
        self.assertEqual(response.status_code, 201)
        response = self.registration('test1', '123456', '1234567')
        self.assertNotEqual(response.status_code, 201)
        response = self.registration('test1', '123456', '123456', 'yao123')
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        """
        Try to login with admin.
        """
        response = self.login('test2', '123456')
        self.assertNotEqual(response.status_code, 200)
        self.registration('test2', '123456', '123456')
        response = self.login('test2', '123456')
        self.assertEqual(response.status_code, 200)

    def test_wechat(self):
        """
        Test to get data from wechat backend.
        """
        response = self.login_for_wechat('123456')
        self.assertNotEqual(response.status_code, 200)

    def test_viewset(self):
        """
        Test if viewset works properly.
        """
        self.login(username='admin',password='123456')
        self.client.login(username='admin', password='123456')
        self.client.get('/api/users/')
        self.client.get('/api/wechat/')

    def test_update(self):
        """
        Test to update user data.
        """
        self.registration('test3','123456','123456')
        self.client.login(username='test3', password='123456')
        data = {
            'username': 'test3',
            'password': '1234567',
            'password_old': '123456',
            'name': 'yaojh',
            'email': 'yaojh18@mails.tsinghua.edu.cn'
        }
        response = self.client.put('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_wechat_serializer(self):
        """
        Because we can't test wechat, so we test how wechat serializer.
        """
        data = {
            'openid': '123456'
        }
        res = WechatLoginSerializer(data=data)
        if res.is_valid():
            self.assertEqual(res.validated_data['openid'], '123456')
            res.save()
        res = WechatLoginSerializer(data=data)
        if res.is_valid():
            res.save()

    def test_token(self):
        """
        Test if token works;
        """
        self.registration('admin', '123456', '123456')
        response = self.login('admin', '123456')
        user = VerifyJSONWebTokenSerializer(data=json.loads(response.content))
        self.assertEqual(user.is_valid(), True)


class WechatTest(TestCase):
    """
    Test wechat serializer.
    """
    def setUp(self):
        user = User.objects.create_superuser(username='admin', password='123456')
        profile = UserProfile(user=user)
        profile.save()
        media = OriginMedia(title="大碗宽面", level_id=0)
        audio = open('data/test/大碗宽面.wav', 'rb+')
        video = open('data/test/大碗宽面.mp4', 'rb+')
        media.video_path.name = 'test/大碗宽面.mp4'
        media.video_path.content = File(video)
        media.audio_path.name = 'test/大碗宽面.wav'
        media.audio_path.content = File(audio)
        media.save()
        video.close()
        audio.close()
        self.client.login(username='admin', password='123456')

    def insert_user_audio(self, level_id=0):
        """
        Insert an user audio.
        """
        audio = open('data/test/大碗宽面.wav', 'rb+')
        data = {
            'level_id': level_id,
            'audio': audio
        }
        response = self.client.post('/api/wechat/audio/', data=data)
        audio.close()
        return response

    def test_profile(self):
        """
        Test API for /api/wechat/profile/.
        """
        data = {
            'gender': 1,
            'nick_name': 'yao123',
            'city': 'beijing',
            'province': 'beijing',
        }
        response = self.client.post('/api/wechat/', data=data)
        self.assertNotEqual(response.status_code, 201)
        data['avatar_url'] = 'https://baidu.com/'
        response = self.client.post('/api/wechat/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_audio(self):
        """
        Test API for /api/wechat/audio/.
        """
        response = self.insert_user_audio(level_id=1)
        self.assertNotEqual(response.status_code, 201)
        response = self.insert_user_audio()
        self.assertEqual(response.status_code, 201)

    def test_level(self):
        """
        Test API for /api/level/.
        """
        self.insert_user_audio()
        data = {
            'level_id': 0
        }
        response = self.client.get('/api/level/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_level_audio(self):
        """
        Test API for /api/level/audio/.
        """
        self.insert_user_audio()
        data = {
            'level_id': 0
        }
        response = self.client.get('/api/level/audio/', data=data)
        self.assertEqual(response.status_code, 200)
        data['level_id'] = 1
        response = self.client.get('/api/level/audio/', data=data)
        self.assertNotEqual(response.status_code, 200)

    def tearDown(self) -> None:
        audios = UserAudio.objects.all()
        global DELETE_FILES
        for audio in audios:
            DELETE_FILES.append(audio.audio.path)
        super().tearDown()


class TrashTest(TestCase):
    """
    Delete the files of test user audios.
    """
    def test_trash(self):
        """
        Delete the files of test user audios.
        """
        global DELETE_FILES
        for file in DELETE_FILES:
            os.remove(file)
