"""
Tests of media app
"""
# pylint: disable=R0913, E5142, C0301
import os
import json
from datetime import datetime
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
        User.objects.create_superuser(username='test', password='123456')
        self.client.login(username='test', password='123456')

    def search(self, level_id=None, title=None, page=None, size=None, type_id=None):
        """
        create search request
        """
        data = dict()
        if level_id is not None:
            data['level_id'] = level_id
        if type_id is not None:
            data['type_id'] = type_id
        if title is not None:
            data['title'] = title
        if page is not None:
            data['page'] = page
        if size is not None:
            data['size'] = size
        return self.client.get('/api/manager/', data=data)

    def create(self, type_id, title, content, audio_path, video_path):
        """
        create add request
        """
        data = {
            'type_id': type_id,
            'title': title,
            'content': content,
            'audio_path': audio_path,
            'video_path': video_path
        }
        response = self.client.post('/api/manager/', data=data)
        return response

    def update(self, data_id, title, content, type_id):
        """
        create edit request
        """
        self.client.login(username='test', password='123456')
        data = {
            'title': title,
            'content': content,
            'type_id': type_id
        }
        return self.client.put('/api/manager/' + str(data_id) + '/',
                               data=data, content_type='application/json')

    def create_list(self, id1, level_id1, id2, level_id2):
        """
        Create a resort list
        """
        data = [
            {
                'id': id1,
                'level_id': level_id1
            },
            {
                'id': id2,
                'level_id': level_id2
            }
        ]
        response = self.client.generic('POST', '/api/manager/resort/',
                                       json.dumps(data), content_type='application/json')
        return response

    def test_create(self):
        """
        test add method
        """
        audio_file, video_file = create_file()
        response = self.create(title='test1', content='test 1',
                               type_id=1,
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
        OriginMedia.objects.create(title='test2', content='test 2',
                                   level_id=0, type_id=1,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        data_id = OriginMedia.objects.all()[0].id
        response = self.update(data_id=data_id, title='test_edit', content='test edit', type_id=0)
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
        response = self.search(level_id=0)
        self.assertEqual(response.status_code, 200)
        response = self.search(type_id=0)
        self.assertEqual(response.status_code, 200)
        response = self.search(title='test')
        self.assertEqual(response.status_code, 200)
        response = self.search(size=2, page=1)
        self.assertEqual(response.status_code, 200)

    def test_resort(self):
        """
        Test resort method.
        """
        media5 = OriginMedia.objects.create(title='test5', content='test 5', level_id=0,
                                   audio_path='/data/origin/audio/test5.wav',
                                   video_path='/data/origin/video/test5.mp4')
        media6 = OriginMedia.objects.create(title='test6', content='test 6', level_id=0,
                                            audio_path='/data/origin/audio/test6.wav',
                                            video_path='/data/origin/video/test6.mp4')
        media7 = OriginMedia.objects.create(title='test7', content='test 7', level_id=0, type_id=1,
                                            audio_path='/data/origin/audio/test7.wav',
                                            video_path='/data/origin/video/test7.mp4')
        response = self.create_list(media5.id, media6.level_id, media6.id + 100, media5.level_id)
        self.assertNotEqual(response.status_code, 200)
        response = self.create_list(media5.id, media6.level_id + 1, media6.id, media5.level_id + 1)
        self.assertNotEqual(response.status_code, 200)
        response = self.create_list(media5.id, media6.level_id, media7.id, media7.level_id)
        self.assertNotEqual(response.status_code, 200)
        response = self.create_list(media5.id, media6.level_id, media6.id, media6.level_id)
        self.assertEqual(response.status_code, 200)




class ClientMediaTest(TestCase):
    """
    Unity tests of media APIs for wechat
    """

    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        self.client.post('/api/users/', data={
            'username': 'test',
            'password': '123456',
            'password_confirm': '123456'
        }, content_type='application/json')
        self.client.login(username='test', password='123456')

    def video(self, level_id, type_id):
        """post for video"""
        data = {
            'level_id': level_id,
            'type_id': type_id
        }
        return self.client.post('/api/media/video/', data=data, content_type='application/json')

    def audio(self, level_id, type_id):
        """post for audio"""
        data = {
            'level_id': level_id,
            'type_id': type_id
        }
        return self.client.post('/api/media/audio/', data=data, content_type='application/json')

    def material(self, level_id, type_id):
        """post for material"""
        data = {
            'level_id': level_id,
            'type_id': type_id
        }
        return self.client.post('/api/media/material/', data=data, content_type='application/json')

    def test_media(self):
        """
        tests for media APIs
        """
        OriginMedia.objects.create(title='test3', content='test 3',
                                   level_id=0, type_id='1',
                                   audio_path='/data/origin/audio/test3.wav',
                                   video_path='/data/origin/video/test3.mp4')
        OriginMedia.objects.create(title='test4', content='test 4',
                                   level_id=1, type_id='2',
                                   audio_path='/data/origin/audio/test4.wav',
                                   video_path='/data/origin/video/test4.mp4')
        response = self.video(level_id=1, type_id=2)
        self.assertEqual(response.status_code, 200)
        response = self.video(level_id=3, type_id=2)
        self.assertEqual(response.status_code, 404)
        response = self.video(level_id='hh', type_id=2)
        self.assertEqual(response.status_code, 400)

        response = self.audio(level_id=0, type_id=1)
        self.assertEqual(response.status_code, 200)
        response = self.audio(level_id=3, type_id=2)
        self.assertEqual(response.status_code, 404)
        response = self.audio(level_id='hh', type_id=2)
        self.assertEqual(response.status_code, 400)

        response = self.material(level_id=0, type_id=1)
        self.assertEqual(response.status_code, 200)
        response = self.material(level_id=3, type_id=2)
        self.assertEqual(response.status_code, 404)
        response = self.material(level_id='hh', type_id=2)
        self.assertEqual(response.status_code, 400)

    def test_list(self):
        """
        tests for list
        """
        response = self.client.get('/api/media/')
        self.assertEqual(response.status_code, 200)


class DataAnalysisTest(TestCase):
    """
    tests for media data analysis APIs
    """
    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        User.objects.create_superuser(username='test', password='123456')
        self.client.login(username='test', password='123456')

    def media(self, title=None, page=None, size=None):
        """
        get media data
        """
        url = '/api/manager/data/origin/?'
        if title is not None:
            url += 'title=' + title + '&'
        if page is not None:
            url += 'page=' + str(page) + '&'
        if size is not None:
            url += 'size=' + str(size) + '&'
        return self.client.get(url, content_type='application/json')

    def user(self, sort=None, gender=None, page=None, size=None):
        """
        get user data
        """
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
        """
        get user audio data
        """
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
        """
        tests for media data APIs
        """
        OriginMedia.objects.create(title='test1', content='test 1', level_id=0,
                                   audio_path='/data/origin/audio/test1.wav',
                                   video_path='/data/origin/video/test1.mp4')
        OriginMedia.objects.create(title='test2', content='test 2', level_id=1,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        response = self.media(title='test', page=1, size=2)
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        """
        tests for user data APIs
        """
        user = User(username='user1', password='123456')
        user.save()
        profile = UserProfile(user=user, openid='1', gender='0')
        profile.save()
        user = User(username='user2', password='123456')
        user.save()
        profile = UserProfile(user=user, openid='2', gender='1')
        profile.save()
        response = self.user(gender=0, page=1, size=2)
        self.assertEqual(response.status_code, 200)

    def test_user_audio(self):
        """
        tests for user audio APIs
        """
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


class ChartTest(TestCase):
    """
    Tests for chart APIs
    """
    def setUp(self):
        Group.objects.create(name='manager')
        Group.objects.create(name='visitor')
        User.objects.create_superuser(username='test', password='123456')
        self.client.login(username='test', password='123456')
        media1 = OriginMedia(title='test1', content='test 1', level_id=0, type_id=1,
                                   audio_path='/data/origin/audio/test1.wav',
                                   video_path='/data/origin/video/test1.mp4')
        media1.save()
        media2 = OriginMedia(title='test2', content='test 2', level_id=0, type_id=2,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        media2.save()
        user = User(username='user1', password='123456')
        user.save()
        UserProfile.objects.create(user=user, openid='hhh', gender=1)
        UserAudio.objects.create(user=user, media=media1, audio='/data/origin/audio/test6.wav',
                         timestamp=datetime(2020, 11, 17, 6, 12, 6, 411666), score=86)
        UserAudio.objects.create(user=user, media=media2, audio='/data/origin/audio/test3.wav',
                         timestamp=datetime(2020, 11, 18, 6, 12, 6, 411666), score=40)
        UserAudio.objects.create(user=user, media=media1, audio='/data/origin/audio/test4.wav',
                         timestamp=datetime(2020, 11, 15, 6, 12, 6, 411666), score=97)
        UserAudio.objects.create(user=user, media=media2, audio='/data/origin/audio/test5.wav',
                         timestamp=datetime(2020, 11, 17, 6, 12, 6, 411666), score=79)

    def media_chart(self, data_id):
        """
        get data for media charts
        """
        return self.client.get('/api/manager/data/origin/'+str(data_id)+'/chart/',
                               content_type='application/json')

    def user_chart(self):
        """
        get data for user charts
        """
        return self.client.get('/api/manager/data/user/chart/',
                               content_type='application/json')

    def user_audio_chart(self):
        """
        get data for user audio charts
        """
        return self.client.get('/api/manager/data/user_audio/chart/',
                               content_type='application/json')

    def test_media_chart(self):
        """
        tests for media charts
        """
        response = self.media_chart(data_id=1)
        self.assertEqual(response.status_code, 200)

    def test_user_chart(self):
        """
        tests for user charts
        """
        response = self.user_chart()
        self.assertEqual(response.status_code, 200)

    def test_user_audio_chart(self):
        """
        tests for user audio charts
        """
        response = self.user_audio_chart()
        self.assertEqual(response.status_code, 200)
