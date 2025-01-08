from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import Task, User

class UserTestCase(APITestCase):
    def setUp(self):
        self.index = 0
        self.url = {
            'register': '/api/user/register',
            'login': '/api/user/login',
            'user': '/api/user/{id}',
        }

    def new_user_data(self):
        data = {
            'username': 'john-doe-{}'.format(self.index),
            'email': 'john-doe-{}@example.com'.format(self.index),
            'password': 'newpass123'
        }
        self.index += 1
        return data 
    

class RegistrationTests(UserTestCase):
    '''
    Test the user registration endpoint
    '''

    # Valid data
    
    def test_success(self):
        user = self.new_user_data() 
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # Invalid data

    def test_invalid_username(self):
        user = self.new_user_data() 
        user['username'] = ''
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        user = self.new_user_data() 
        user['email'] = ''
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        user = self.new_user_data()
        user['password'] = ''
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    # User already exists

    def test_duplicate_username(self):
        existing_user = self.new_user_data()
        User.objects.create_user(**existing_user)

        user = self.new_user_data()
        user['username'] = existing_user['username']
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        existing_user = self.new_user_data()    
        User.objects.create_user(**existing_user)

        user = self.new_user_data()
        user['email'] = existing_user['email']
        res = self.client.post(self.url['register'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTests(UserTestCase):
    '''
    Test the user login endpoint
    '''
    
    # Valid data

    def test_success(self):
        user = self.new_user_data()
        User.objects.create_user(**user)
        res = self.client.post(self.url['login'], user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Invalid data

    def test_invalid_username(self):
        user = self.new_user_data()
        user['username'] = ''
        res = self.client.post(self.url['login'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        user = self.new_user_data()
        user['password'] = ''
        res = self.client.post(self.url['login'], user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Incorrect data

    def test_incorrect_username(self):
        user = self.new_user_data()
        user['username'] = 'incorrect_username'
        res = self.client.post(self.url['login'], user)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_incorrect_password(self):
        user = self.new_user_data()
        user['password'] = 'incorrect_password'
        res = self.client.post(self.url['login'], user)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
