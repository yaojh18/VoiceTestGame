"""
Tests of media app
"""
# pylint: disable=R0913
import os
import json
from django.test import TestCase
from django.contrib.auth.models import Group, User
from personnel.models import UserProfile, UserAudio
from .models import OriginMedia


def create_file():
    """
    create test files
    """
    cwd = os.getcwd()
    if not os.path.exists(cwd + '/data/test/'):
        os.mkdir(cwd + '/data/test/')
    file = open(cwd + '/data/test/audio.txt', 'w')
    file.write('this is an audio')
    file.close()
    file = open(cwd + '/data/test/video.txt', 'w')
    file.write('this is a video')
    file.close()
    audio_file = open(cwd + '/data/test/audio.txt')
    video_file = open(cwd + '/data/test/video.txt')
    return audio_file, video_file


class ManagerTest(TestCase):
    """
    Unity tests of ManagerViewSets
    """

    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        response = self.client.post('/api/users/registration/', data={
            'username': 'test',
            'password': '123456',
            'password2': '123456'
        }, content_type='application/json')
        self.token = json.loads(response.content)["token"]
        self.client.login(username='test', password='123456')

    def search(self, level=None, name=None, page=None, size=None):
        """
        create search request
        """
        url = '/api/manager/?'
        if level is not None:
            url += 'level=' + str(level) + '&'
        if name is not None:
            url += 'title=' + name + '&'
        if page is not None:
            url += 'page_limit=' + str(page) + '&'
        if size is not None:
            url += 'size=' + str(size) + '&'
        return self.client.get(url, content_type='application/json')

    def create(self, title, content, audio_path, video_path):
        """
        create add request
        """
        data = {
            'level_id': '',
            'title': title,
            'content': content,
            'audio_path': audio_path,
            'video_path': video_path
        }
        return self.client.post('/api/manager/', data=data)

    def update(self, data_id, level_id, title, content, audio_path=None, video_path=None):
        """
        create edit request
        """
        data = {
            'level_id': level_id,
            'title': title,
            'content': content,
            'audio_path': None,
            'video_path': None
        }
        return self.client.put('/api/manager/' + str(data_id) + '/', data=data, content_type='application/json')

    def test_create(self):
        """
        test add method
        """
        audio_file, video_file = create_file()
        response = self.create(title='test1', content='test 1',
                               audio_path=audio_file,
                               video_path=video_file)
        self.assertEqual(response.status_code, 201)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/data/origin/audio/audio.txt'):
            os.remove(cwd + '/data/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/data/origin/video/video.txt'):
            os.remove(cwd + '/data/origin/video/video.txt')

    def test_update(self):
        """
        test edit method
        """
        OriginMedia.objects.create(title='test2', content='test 2', level_id=0,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        data_id = OriginMedia.objects.all()[0].id
        response = self.update(data_id=data_id, title='test_edit', content='test edit', level_id=0)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        """
        test search method
        """
        OriginMedia.objects.create(title='test3', content='test 3', level_id=0,
                                   audio_path='/data/origin/audio/test3.wav',
                                   video_path='/data/origin/video/test3.mp4')
        OriginMedia.objects.create(title='test4', content='test 4', level_id=1,
                                   audio_path='/data/origin/audio/test4.wav',
                                   video_path='/data/origin/video/test4.mp4')
        response = self.search()
        self.assertEqual(response.status_code, 200)
        response = self.search(level=0)
        self.assertEqual(response.status_code, 200)
        response = self.search(name='test')
        self.assertEqual(response.status_code, 200)
        response = self.search(size=2, page=1)
        self.assertEqual(response.status_code, 200)


class ClientMediaTest(TestCase):
    """
    Unity tests of media APIs for wechat
    """

    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        response = self.client.post('/api/users/registration/', data={
            'username': 'test',
            'password': '123456',
            'password2': '123456'
        }, content_type='application/json')
        self.token = json.loads(response.content)["token"]
        self.client.login(username='test', password='123456')

    def video(self, level_id):
        data = {
            'level_id': level_id
        }
        return self.client.post('/api/media/video/', data=data, content_type='application/json')

    def audio(self, level_id):
        data = {
            'level_id': level_id
        }
        return self.client.post('/api/media/audio/', data=data, content_type='application/json')

    def material(self, level_id):
        data = {
            'level_id': level_id
        }
        return self.client.post('/api/media/material/', data=data, content_type='application/json')

    def test_media(self):
        OriginMedia.objects.create(title='test3', content='test 3', level_id=0,
                                   audio_path='/data/origin/audio/test3.wav',
                                   video_path='/data/origin/video/test3.mp4')
        OriginMedia.objects.create(title='test4', content='test 4', level_id=1,
                                   audio_path='/data/origin/audio/test4.wav',
                                   video_path='/data/origin/video/test4.mp4')
        # print(OriginMedia.objects.all().values())
        response = self.video(level_id=1)
        self.assertEqual(response.status_code, 200)
        response = self.video(level_id=3)
        self.assertEqual(response.status_code, 404)
        response = self.video(level_id='hh')
        self.assertEqual(response.status_code, 400)

        response = self.audio(level_id=0)
        self.assertEqual(response.status_code, 200)
        response = self.audio(level_id=3)
        self.assertEqual(response.status_code, 404)
        response = self.audio(level_id='hh')
        self.assertEqual(response.status_code, 400)

        response = self.material(level_id=0)
        self.assertEqual(response.status_code, 200)
        response = self.material(level_id=3)
        self.assertEqual(response.status_code, 404)
        response = self.material(level_id='hh')
        self.assertEqual(response.status_code, 400)

    def test_list(self):
        response = self.client.get('/api/media/')
        self.assertEqual(response.status_code, 200)


class DataAnalysisTest(TestCase):
    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        response = self.client.post('/api/users/registration/', data={
            'username': 'test',
            'password': '123456',
            'password2': '123456'
        }, content_type='application/json')
        self.token = json.loads(response.content)["token"]
        self.client.login(username='test', password='123456')

    def media(self, title=None, page=None, size=None):
        url = '/api/manager/data/origin/?'
        if title is not None:
            url += 'title=' + title + '&'
        if page is not None:
            url += 'page=' + str(page) + '&'
        if size is not None:
            url += 'size=' + str(size) + '&'
        return self.client.get(url, content_type='application/json')

    def user(self, sort=None, gender=None, page=None, size=None):
        url = '/api/manager/data/user/?'
        if sort is not None:
            url += 'sort=' + sort + '&'
        if gender is not None:
            url += 'gender=' + str(gender) + '&'
        if page is not None:
            url += 'page=' + str(page) + '&'
        if size is not None:
            url += 'size=' + str(size) + '&'
        return self.client.get(url, content_type='application/json')

    def user_audio(self, level=None, gender=None, start_time=None, end_time=None, sort=None):
        url = '/api/manager/data/user_audio/?'
        if level is not None:
            url += 'level=' + str(level) + '&'
        if sort is not None:
            url += 'sort=' + sort + '&'
        if gender is not None:
            url += 'gender=' + str(gender) + '&'
        if start_time is not None:
            url += 'start_time=' + start_time + '&'
        if end_time is not None:
            url += 'end_time=' + end_time + '&'
        return self.client.get(url, content_type='application/json')

    def test_media(self):
        OriginMedia.objects.create(title='test1', content='test 1', level_id=0,
                                   audio_path='/data/origin/audio/test1.wav',
                                   video_path='/data/origin/video/test1.mp4')
        OriginMedia.objects.create(title='test2', content='test 2', level_id=1,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        response = self.media(title='test', page=1, size=2)
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        user = User(username='user1', password='123456')
        user.save()
        profile = UserProfile(user=user, openid='1', gender='0', level=0)
        profile.save()
        user = User(username='user2', password='123456')
        user.save()
        profile = UserProfile(user=user, openid='2', gender='1', level=3)
        profile.save()
        response = self.user(sort='level', gender=0, page=1, size=2)
        self.assertEqual(response.status_code, 200)

    def test_user_audio(self):
        user = User(username='user1', password='123456')
        user.save()
        media = OriginMedia(title='test1', content='test 1', level_id=0,
                            audio_path='/data/origin/audio/test1.wav',
                            video_path='/data/origin/video/test1.mp4')
        media.save()
        audio = UserAudio(user=user, media=media, audio='/data/origin/audio/test1.wav')
        audio.save()
        response = self.user_audio(level=0, gender=0, sort='score')
        self.assertEqual(response.status_code, 200)
        response = self.user_audio(sort='level', start_time='2020-11-3')
        self.assertEqual(response.status_code, 200)
        response = self.user_audio(sort='time', end_time='2020-11-5')
        self.assertEqual(response.status_code, 200)
