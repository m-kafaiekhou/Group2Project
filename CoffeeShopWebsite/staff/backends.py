from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from .models import CustomUserModel


class CustomUserBackend(ModelBackend):
    UserModel = CustomUserModel

    # def authenticate(self, request, phone_number=None, password=None, **kwargs):
    #     username = phone_number

    #     if username is None:
    #         username = kwargs.get(self.UserModel.USERNAME_FIELD)
    #     if username is None or password is None:
    #         return
    #     try:
    #         user = self.UserModel._default_manager.get_by_natural_key(username)
    #     except self.UserModel.DoesNotExist:
    #         # Run the default password hasher once to reduce the timing
    #         # difference between an existing and a nonexistent user (#20760).
    #         self.UserModel().set_password(password)
    #     else:
    #         if user.check_password(password) and self.user_can_authenticate(user):
    #             return user

    def authenticate(self, request, phone_number=None, otp_code=None, **kwargs):
        username = phone_number

        if username is None:
            username = kwargs.get(self.UserModel.USERNAME_FIELD)
        if username is None or otp_code is None:
            return
