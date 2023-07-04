from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from social.models import Post, Hashtags
from social.permissions import IsAdminOrIfAuthenticatedReadOnly
from social.serializers import PostSerializer, HashtagsSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    Posts create and list view with filtering by hashtags id.
    User can see only owns posts and posts their following users
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        if self.action == "list":
            following_ids = self.request.user.following.values_list(
                'id', flat=True
            )

            queryset = Post.objects.filter(
                Q(creator=self.request.user) |
                Q(creator_id__in=following_ids)
            )

            hashtags = self.request.query_params.get("hashtags")

            if hashtags:
                hashtags_id = self._params_to_ints(hashtags)
                queryset = queryset.filter(hashtags__id__in=hashtags_id)
            return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by hashtags id (ex. ?hashtags=2,5)",
            ),

        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HashtagsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Hashtags create and get view"""
    queryset = Hashtags.objects.all()
    serializer_class = HashtagsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

