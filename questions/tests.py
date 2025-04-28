from django.test import TestCase
from rest_framework.test import APIClient
from oauth2_provider.models import Application
from urllib.parse import urlencode
from .models import Question
from users.models import CustomUser


class QuestionsTests(TestCase):
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

        # Authenticate and get access token
        token_url = '/o/token/'
        token_data = {
            'grant_type': 'password',
            'username': 'abhishek',
            'password': 'strongpassword123',
            'client_id': "myclientid123",
            'client_secret': "myclientsecret456",
        }
        encoded_data = urlencode(token_data)
        token_response = self.client.post(token_url, data=encoded_data,
                                          content_type="application/x-www-form-urlencoded")
        self.access_token = token_response.json()['access_token']

        # Authorization header for client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_question(self):
        url = '/api/questions/'
        data = {
            'title': 'How to use Django for APIs?',
            'body': 'I want to learn how Django can be used to create REST APIs.',
            'tags': "django, api"
        }

        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'How to use Django for APIs?')

    def test_list_questions(self):
        # First create a question
        Question.objects.create(title='Test Title', body='Test content', author=self.user)

        url = '/api/questions/'
        response = self.client.get(url)
        print("response--", response)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        print(response.data)

    def test_update_question(self):
        question = Question.objects.create(title='Old Title', body='Old content', author=self.user)

        url = f'/api/questions/{question.id}/'
        data = {
            'title': 'Updated Title',
            'body': 'Updated content',
            'tags': "test, api"
        }

        response = self.client.put(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_question(self):
        question = Question.objects.create(title='Delete me', body='This question will be deleted', author=self.user)

        url = f'/api/questions/{question.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Make sure it is actually deleted
        self.assertFalse(Question.objects.filter(id=question.id).exists())
