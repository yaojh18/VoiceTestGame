"""
Tests of media app
"""
from django.test import TestCase
from .models import OriginMedia
from django.core.files.uploadedfile import UploadedFile
import os

class ManagerTest(TestCase):
    """
    Unity tests of ManagerViewSets
    """

    def setUp(self):
        OriginMedia.objects.create(title='test1', content='test 1',
                                   audio_path='/media/origin/audio/test1.wav',
                                   video_path='/media/origin/video/test1.mp4')
        OriginMedia.objects.create(title='test2', content='test 2',
                                   audio_path='/media/origin/audio/test2.wav',
                                   video_path='/media/origin/video/test2.mp4')
        # print(OriginMedia.objects.values())

    def create_file(self):
        if not os.path.exists('./media/media/test/'):
            os.mkdir('./media/media/test/')
        f = open('./media/media/test/audio.txt', 'w')
        f.write('this is an audio')
        f.close()
        f = open('./media/media/test/video.txt', 'w')
        f.write('this is a video')
        f.close()
        audio_file = open('./media/media/test/audio.txt')
        video_file = open('./media/media/test/video.txt')
        return audio_file, video_file

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

    def test_search(self):
        """
        test search method
        """
        response = self.search(data_id=6)
        self.assertEqual(response.status_code, 200)
        response = self.search(data_id=8)
        self.assertEqual(response.status_code, 404)
        response = self.search(data_id='ab')
        self.assertEqual(response.status_code, 400)

    def test_add(self):
        """
        test add method
        """
        audio_file, video_file = self.create_file()
        response = self.add(title='test3', content='test 3',
                            audio_path=audio_file,
                            video_path=video_file)
        # print('test_add_201:', response)
        self.assertEqual(response.status_code, 201)

        audio_file, video_file = self.create_file()
        response = self.add(title='test3', content='',
                            audio_path=audio_file,
                            video_path=video_file)
        # print('test_add_403:', response)
        self.assertEqual(response.status_code, 400)

        # os.remove('./media/media/test/audio.txt')
        # os.remove('./media/media/test/video.txt')
        # os.rmdir('./media/media/test/')

    def test_edit(self):
        """
        test edit method
        """
        audio_file, video_file = self.create_file()
        response = self.edit(data_id=4, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        # print('test_edit_201:', response)
        self.assertEqual(response.status_code, 201)

        audio_file, video_file = self.create_file()
        response = self.edit(data_id=101, title='test_edit', content='test edit',
                             audio_path=audio_file,
                             video_path=video_file)
        # print('test_edit_404:', response)
        self.assertEqual(response.status_code, 404)

        audio_file, video_file = self.create_file()
        response = self.edit(data_id='hh', title='', content='',
                             audio_path=audio_file,
                             video_path=video_file)
        # print('test_edit_400:', response)
        self.assertEqual(response.status_code, 400)
