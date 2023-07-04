from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet

from social.models import Post
from social.serializers import PostSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.action == "list":
            queryset = Post.objects.filter(
                Q(creator=self.request.user) |
                Q(creator__follow__follower_user__id=self.request.user.id)
            )
            return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)