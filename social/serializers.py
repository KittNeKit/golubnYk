from rest_framework import serializers

from social.models import Follow, Post


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = None # todo fields


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("creator", "text")
        read_only_fields = ("creator",)
