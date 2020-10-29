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

    def search(self, data_id=None):
        """
        create search request
        """
        data = {
            'id': data_id,
            'Authorization': 'JWT ' + self.token
        }
        return self.client.post('/api/manager/search/', data=data, content_type='application/json',
                                **{'Authorization': 'JWT ' + self.token})

    def add(self, title, content, audio_path, video_path):
        """
        create add request
        """
        data = {
            'title': title,
            'content': content,
            'audio_path': audio_path,
            'video_path': video_path
        }
        return self.client.post('/api/manager/add/', data=data)

    def edit(self, data_id, title, content, audio_path, video_path):
        """
        create edit request
        """
        data = {
            'id': data_id,
            'title': title,
            'content': content,
            'audio_path': audio_path,
            'video_path': video_path
        }
        return self.client.post('/api/manager/edit/', data=data)

    def test_add(self):
        """
        test add method
        """
        audio_file, video_file = create_file()
        response = self.add(title='test1', content='test 1',
                            audio_path=audio_file,
                            video_path=video_file)
        self.assertNotEqual(response.status_code, 201)

        audio_file, video_file = create_file()
        response = self.add(title='test1', content='',
                            audio_path=audio_file,
                            video_path=video_file)
        self.assertNotEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/data/origin/audio/audio.txt'):
            os.remove(cwd + '/data/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/data/origin/video/video.txt'):
            os.remove(cwd + '/data/origin/video/video.txt')
        # os.rmdir(cwd+'/data/test/')

    """
    def test_edit(self):
        audio_file, video_file = create_file()
        OriginMedia.objects.create(title='test2', content='test 2', media_id=0,
                                   audio_path='/data/origin/audio/test2.wav',
                                   video_path='/data/origin/video/test2.mp4')
        response = self.edit(data_id=0, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertNotEqual(response.status_code, 201)

        audio_file, video_file = create_file()
        response = self.edit(data_id=101, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertNotEqual(response.status_code, 404)

        audio_file, video_file = create_file()
        response = self.edit(data_id='hh', title='', content='',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertNotEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/data/origin/audio/audio.txt'):
            os.remove(cwd + '/data/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/data/origin/video/video.txt'):
            os.remove(cwd + '/data/origin/video/video.txt')

    def test_search(self):
        OriginMedia.objects.create(title='test3', content='test 3', media_id=0,
                                   audio_path='/data/origin/audio/test3.wav',
                                   video_path='/data/origin/video/test3.mp4')
        OriginMedia.objects.create(title='test4', content='test 4', media_id=1,
                                   audio_path='/data/origin/audio/test4.wav',
                                   video_path='/data/origin/video/test4.mp4')
        response = self.search(data_id=0)
        self.assertNotEqual(response.status_code, 200)
        response = self.search(data_id=8)
        self.assertNotEqual(response.status_code, 404)
        response = self.search(data_id='ab')
        self.assertNotEqual(response.status_code, 400)
    """
