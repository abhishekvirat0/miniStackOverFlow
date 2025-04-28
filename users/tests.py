from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from oauth2_provider.models import Application
from rest_framework import status
from urllib.parse import urlencode


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='abhishek',
            password='strongpassword123',
            email='abhishek@example.com'
        )

        self.application = Application.objects.create(
            name="Test Application",
            client_id="myclientid123",
            client_secret="myclientsecret456",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            skip_authorization=True,
            user=self.user,
        )
        self.application.save()

    def test_register_user(self):
        url = '/api/users/register/'
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com'
        }

        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], 'newuser')

    def test_login_user(self):
        url = '/o/token/'
        data = {
            'grant_type': 'password',
            'username': 'abhishek',
            'password': 'strongpassword123',
            'client_id': "myclientid123",
            'client_secret': "myclientsecret456",
        }
        encoded_data = urlencode(data)
        print(f"Request Data: {data}")

        response = self.client.post(url, data=encoded_data, content_type="application/x-www-form-urlencoded")

        print(f"Response JSON: {response.json()}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

    def test_profile_me(self):
        token_url = '/o/token/'
        token_data = {
            'grant_type': 'password',
            'username': 'abhishek',
            'password': 'strongpassword123',
            'client_id': "myclientid123",
            'client_secret': "myclientsecret456",
        }
        encoded_data = urlencode(token_data)
        token_response = self.client.post(token_url,
                                          data=encoded_data,
                                          content_type="application/x-www-form-urlencoded")  # Send as JSON
        print(token_response)
        access_token = token_response.json()['access_token']

        # call the /api/users/me/ endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], 'abhishek')
