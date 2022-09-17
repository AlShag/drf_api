from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views.login_view import LoginView
from accounts.views.logout_view import LogoutView
from accounts.views.sign_up_view import SignUpView
from accounts.views.user_view_set import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/sign-up/", SignUpView.as_view(), name="sign-up"),
    *router.urls,
]
