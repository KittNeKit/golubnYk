from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import UserCreateView, ManageUserView, UsersViewSet


router = routers.DefaultRouter()
router.register("users", UsersViewSet)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage"),
] + router.urls

app_name = "user"
