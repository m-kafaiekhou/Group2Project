from django.urls import path
from .views import LoginUserView

app_name = "staff"
urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
]
