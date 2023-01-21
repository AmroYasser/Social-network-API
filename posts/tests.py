from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.urls import reverse
from .views import PostViewSet
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostViewSet.as_view({"get": "list", "post": "create"})
        self.url = reverse("post_list")
        self.user = User.objects.create_user(
            email="testuser@gmail.com", name="testuser"
        )
        self.user.set_password("pass")
        self.user.save()

    def test_list_posts(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        print(User)
        print(self.user)
        self.client.login(email="testuser@gmail.com", password="pass")
        sample_post = {
            "title": "sample title",
            "body": "sample body",
        }
        response = self.client.post("/posts/", sample_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
