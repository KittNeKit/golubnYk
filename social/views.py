from django.db.models import Q

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from social.models import Post, Hashtags
from social.serializers import PostSerializer, HashtagsSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        if self.action == "list":
            # queryset = Post.objects.filter(
            #     Q(creator=self.request.user)
            # )

            queryset = self.queryset
            hashtags = self.request.query_params.get("hashtags")

            if hashtags:
                hashtags_id = self._params_to_ints(hashtags)
                queryset = queryset.filter(hashtags__id__in=hashtags_id)
            return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HashtagsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Hashtags.objects.all()
    serializer_class = HashtagsSerializer
