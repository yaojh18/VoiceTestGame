"""
Tests of media app
"""
from django.test import TestCase


class ManagerTest(TestCase):
    """
    tests of ManagerViewSets
    """
    def search(self, data_id=None):
        """
        create post request of search
        """
        data = {
            'id': data_id
        }
        return self.client.post('api/manager/search/', data=data, content_type='application/json')

    def test_search(self):
        """
        search: test case 1
        """
        response = self.search(1)
        self.assertEqual(response.status_code, 404)
