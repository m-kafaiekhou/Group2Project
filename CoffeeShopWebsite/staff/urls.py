from django.urls import path
from .views import CustomUserLoginView, CustomUserLoginVerifyView

urlpatterns = [
    path("login/", CustomUserLoginView.as_view(), name="login"),
    path("verify", CustomUserLoginVerifyView.as_view(), name="verify"),
]
