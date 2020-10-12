"""
Tests of media app
"""
# pylint: disable=R0913
import os
from django.test import TestCase
from .models import OriginMedia


def create_file():
    """
    create test files
    """
    cwd = os.getcwd()
    if not os.path.exists(cwd+'/media/media/test/'):
        os.mkdir(cwd+'/media/media/test/')
    file = open(cwd+'/media/media/test/audio.txt', 'w')
    file.write('this is an audio')
    file.close()
    file = open(cwd+'/media/media/test/video.txt', 'w')
    file.write('this is a video')
    file.close()
    audio_file = open(cwd+'/media/media/test/audio.txt')
    video_file = open(cwd+'/media/media/test/video.txt')
    return audio_file, video_file


class ManagerTest(TestCase):
    """
    Unity tests of ManagerViewSets
    """

    def search(self, data_id=None):
        """
        create search request
        """
        data = {
            'id': data_id
        }
        return self.client.post('/api/manager/search/', data=data, content_type='application/json')

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
        self.assertEqual(response.status_code, 201)

        audio_file, video_file = create_file()
        response = self.add(title='test1', content='',
                            audio_path=audio_file,
                            video_path=video_file)
        self.assertEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd+'/media/media/origin/audio/audio.txt'):
            os.remove(cwd+'/media/media/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/media/media/origin/video/video.txt'):
            os.remove(cwd+'/media/media/origin/video/video.txt')
        # os.rmdir(cwd+'/media/media/test/')

    def test_edit(self):
        """
        test edit method
        """
        audio_file, video_file = create_file()
        OriginMedia.objects.create(title='test2', content='test 2',
                                   audio_path='/media/origin/audio/test2.wav',
                                   video_path='/media/origin/video/test2.mp4')
        response = self.edit(data_id=2, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertEqual(response.status_code, 201)

        audio_file, video_file = create_file()
        response = self.edit(data_id=101, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertEqual(response.status_code, 404)

        audio_file, video_file = create_file()
        response = self.edit(data_id='hh', title='', content='',
                             audio_path=audio_file,
                             video_path=video_file)
        self.assertEqual(response.status_code, 400)

        cwd = os.getcwd()
        if os.path.isfile(cwd + '/media/media/origin/audio/audio.txt'):
            os.remove(cwd + '/media/media/origin/audio/audio.txt')
        if os.path.isfile(cwd + '/media/media/origin/video/video.txt'):
            os.remove(cwd + '/media/media/origin/video/video.txt')

    def test_search(self):
        """
        test search method
        """
        OriginMedia.objects.create(title='test3', content='test 3',
                                   audio_path='/media/origin/audio/test3.wav',
                                   video_path='/media/origin/video/test3.mp4')
        OriginMedia.objects.create(title='test4', content='test 4',
                                   audio_path='/media/origin/audio/test4.wav',
                                   video_path='/media/origin/video/test4.mp4')
        response = self.search(data_id=3)
        self.assertEqual(response.status_code, 200)
        response = self.search(data_id=8)
        self.assertEqual(response.status_code, 404)
        response = self.search(data_id='ab')
        self.assertEqual(response.status_code, 400)
