from django.urls import path
from .views import LoginUserView
from django.contrib.auth.views import LogoutView

app_name = "staff"
urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),
]
