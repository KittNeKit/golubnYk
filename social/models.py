from django.conf import settings
from django.db import models

from user.models import User


class Hashtags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    text = models.TextField()
    hashtags = models.ManyToManyField(Hashtags, related_name="post", null=True)
