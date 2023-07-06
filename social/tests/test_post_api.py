from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from social.models import Post
from social.serializers import PostSerializer

POST_URL = reverse("social:post-list")


def detail_url(post_id):
    return reverse("social:post-detail", args=[post_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_post(creator, **params):
    defaults = {
        "creator": creator,
        "text": "Some text for some test post",
    }
    defaults.update(params)

    return Post.objects.create(**defaults)


class PublicOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="tests@test.com",
            username="test_post",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_movies(self):
        sample_post(self.user)

        response = self.client.get(POST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_movie(self):
        post = sample_post(self.user)

        url = detail_url(post.id)
        serializer = PostSerializer(post, many=False)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_posts(self):
        payload = {
            "creator": self.user,
            "text": "Some text for some test post",
        }

        response = self.client.post(POST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
