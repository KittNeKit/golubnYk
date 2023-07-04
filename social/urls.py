from rest_framework import routers

from social.views import PostViewSet, HashtagsViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("hashtags", HashtagsViewSet)

urlpatterns = [
] + router.urls

app_name = "social"
