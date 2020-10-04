from django.test import TestCase
from .models import *

class ManagerTest(TestCase):
    # def setUp(self):
    #     pass

    def search(self, data_id=None):
        data = {
            'id': data_id
        }
        return self.client.post('api/manager/search/', data=data, content_type='application/json')

    def test_search(self):
        response = self.search(1)
        print(response.status_code)
        self.assertEqual(response.status_code, 404)

