"""
TODO
"""
from django.test import TestCase
<<<<<<< HEAD

=======
>>>>>>> 7c21844ddffdcffc15373c4183e60b4c9307913c

class ManagerTest(TestCase):
    """
    TODO
    """
    def search(self, data_id=None):
        """
        TODO
        """
        data = {
            'id': data_id
        }
        return self.client.post('api/manager/search/', data=data, content_type='application/json')

    def test_search(self):
        """
        TODO
        """
        response = self.search(1)
        print(response.status_code)
        self.assertEqual(response.status_code, 404)
