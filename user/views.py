from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """User creation view"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Personal profile view"""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    List and Detail view for users profile with filtering by username
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by username (ex. ?username=kittnekit)",
            ),

        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        """Follow function"""
        user = self.get_object()
        follower = self.request.user

        if follower == user:
            return Response({'error': 'You cannot follow yourself.'}, status=400)

        user.followers.add(follower)
        return Response({'success': 'You are now following this user.'}, status=200)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow function"""
        user = self.get_object()
        follower = request.user

        if follower == user:
            return Response({'error': 'You cannot unfollow yourself.'}, status=400)

        user.followers.remove(follower)
        return Response({'success': 'You have unfollowed this user.'}, status=200)


class APILogoutView(APIView):
    """
    Logout and invalidate token view.

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})
