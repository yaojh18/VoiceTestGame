"""
Unity test for personnel.
"""
from django.test import TestCase
import requests

# Create your tests here.

class LogTest(TestCase):
    """
    Unity test for Login and Registration.
    """
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

WEAPP_ID = 'wxcec8955125bd6732'
WEAPP_SECRETE = 'd26321578e183029be05d63ac982a660'
def getWechatCredential(code):
    auth_url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = dict()
    params['appid'] = WEAPP_ID
    params['secret'] = WEAPP_SECRETE
    params['js_code'] = code
    params['grant_type'] = 'authorization_code'
    login_response = requests.get(auth_url, params=params)
    login_response = login_response.json()
    return login_response


login_response = getWechatCredential("")
print(login_response)