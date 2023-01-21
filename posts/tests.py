from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.urls import reverse
from .views import PostViewSet


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostViewSet.as_view({"get": "list", "post": "create"})
        self.url = reverse("post_list")

    def test_list_posts(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
