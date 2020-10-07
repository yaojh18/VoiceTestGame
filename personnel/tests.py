"""
Unity test for personnel.
"""
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create your tests here.

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
        return self.client.post('/api/users/login/', data=data,
                                content_type='application/json')

    def registration(self, username=None, password=None, password2=None):
        """
        Registration method.
        """
        data = {
            'username': username,
            'password': password,
            'password2': password2
        }
        return self.client.post('/api/users/registration/', data=data,
                                content_type='application/json')

    def login_for_wechat(self, session_id=None):
        """
        Login method for wechat.
        """
        data = {
            "code": session_id
        }
        return self.client.post('/api/wechat/login/', data=data,
                                content_type='application/json')

    def test_login(self):
        """
        Try to login with admin.
        """
        response = self.login('admin', '123456')
        print(response.status_code)
        self.assertIs(response.status_code, 200)

    def test_registration(self):
        """
        Try to create test account.
        """
        response = self.registration('test', '123456', '123456')
        self.assertIs(response.status_code, 200)

    def test_wechat(self):
        """
        Test to get data from wechat backend.
        """
        response = self.login_for_wechat('123456')
        self.assertIs(response.status_code, 200)
        print(response)
