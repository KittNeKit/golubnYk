from django.urls import path
from rest_framework import routers

from social.views import PostViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
] + router.urls

app_name = "social"
