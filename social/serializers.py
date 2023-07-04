from rest_framework import serializers

from social.models import Post, Hashtags


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("creator", "text", "hashtags")
        read_only_fields = ("creator",)


class HashtagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtags
        fields = "name",
