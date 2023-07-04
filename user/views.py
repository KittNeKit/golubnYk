from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
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
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user = self.get_object()
        follower = self.request.user  # Assuming you have authentication set up

        if follower == user:
            return Response({'error': 'You cannot follow yourself.'}, status=400)

        user.followers.add(follower)
        return Response({'success': 'You are now following this user.'}, status=200)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        follower = request.user  # Assuming you have authentication set up

        if follower == user:
            return Response({'error': 'You cannot unfollow yourself.'}, status=400)

        user.followers.remove(follower)
        return Response({'success': 'You have unfollowed this user.'}, status=200)