from rest_framework.test import APITestCase
from rest_framework import status


class RegisterationTestCase(APITestCase):
    def test_registeration(self):
        data = {"email": "test@gmail.com", "name": "test_user", "password": "pass"}
        response = self.client.post("/account/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
