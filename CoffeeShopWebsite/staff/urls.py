from django.urls import path
from .views import CustomUserLoginView

urlpatterns = [
    path("login/", CustomUserLoginView.as_view(), name="c-login"),
]
