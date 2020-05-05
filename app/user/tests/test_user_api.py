from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

TEST_USER = {
    'email': 'Test@Test.com',
    'password': 'TestPass',
    'name': 'Test Name',
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test user API-public"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid
        payload is successful"""

        res = self.client.post(CREATE_USER_URL,
                               TEST_USER)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(TEST_USER['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exist fails"""

        create_user(**TEST_USER)

        res = self.client.post(CREATE_USER_URL, TEST_USER)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Test that the password must be more than 5 characters"""
        test_user = {
            'email': 'Test@Test.com',
            'password': 'pw',
        }

        res = self.client.post(CREATE_USER_URL, test_user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=test_user.get('email')
        ).exists()
        self.assertFalse(user_exists)
