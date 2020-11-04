"""
Tests of media app
"""
# pylint: disable=R0913
import os
import json
from django.test import TestCase
from django.contrib.auth.models import Group
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

    def search(self, level=None, name=None, page_limit=None, page_start=None):
        """
        create search request
        """
        url = '/api/manager/?'
        if level is not None:
            url += 'level=' + str(level) + '&'
        if name is not None:
            url += 'title=' + name + '&'
        if page_limit is not None:
            url += 'page_limit=' + str(page_limit) + '&'
        if page_start is not None:
            url += 'page_start=' + str(page_start) + '&'
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

    def update(self, data_id, level_id, title, content, audio_path, video_path):
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
        # print(response.content)
        self.assertEqual(response.status_code, 201)

        # audio_file, video_file = create_file()
        # response = self.create(title='test1', content='',
        #                        audio_path=audio_file,
        #                        video_path=video_file)
        # self.assertEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/data/origin/audio/audio.txt'):
            os.remove(cwd + '/data/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/data/origin/video/video.txt'):
            os.remove(cwd + '/data/origin/video/video.txt')
        # os.rmdir(cwd+'/data/test/')

    def test_update(self):
        """
        test edit method
        """
        audio_file, video_file = create_file()
        OriginMedia.objects.create(title='test2', content='test 2', level_id=0,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        # print(OriginMedia.objects.values())
        data_id = OriginMedia.objects.all()[0].id
        response = self.update(data_id=data_id, title='test_edit', content='test edit',
                               level_id=0,
                               audio_path=audio_file,
                               video_path=video_file)
        # print(response.content)
        self.assertEqual(response.status_code, 200)

        # audio_file, video_file = create_file()
        # response = self.edit(data_id=101, title='test_edit', content='test edit',
        #                      audio_path=audio_file,
        #                      video_path=video_file)
        # self.assertEqual(response.status_code, 404)

        # audio_file, video_file = create_file()
        # response = self.edit(data_id='hh', title='', content='',
        #                      audio_path=audio_file,
        #                      video_path=video_file)
        # self.assertEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/data/origin/audio/audio.txt'):
            os.remove(cwd + '/data/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/data/origin/video/video.txt'):
            os.remove(cwd + '/data/origin/video/video.txt')

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
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        response = self.search(level=0)
        self.assertEqual(response.status_code, 200)
        response = self.search(name='test')
        self.assertEqual(response.status_code, 200)
        response = self.search(page_limit=2, page_start=0)
        self.assertEqual(response.status_code, 200)

        # response = self.search(data_id=8)
        # self.assertEqual(response.status_code, 404)
        # response = self.search(data_id='ab')
        # self.assertEqual(response.status_code, 400)


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
