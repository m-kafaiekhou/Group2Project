from django.urls import path

urlpatterns = [
    path("login/", CustomUserLoginView.as_view(), name="login"),
    path("verify/", CustomUserLoginVerifyView.as_view(), name="verify"),
]
