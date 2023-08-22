from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import CustomUserModel
import datetime
from menus.models import CafeItem, Category
from order.models import Order, OrderItem
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



class CustomUserBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, otp_code=None, **kwargs):
        username = phone_number

        if username is None:
            username = kwargs.get(CustomUserModel.USERNAME_FIELD)
        if username is None or otp_code is None:
            return
        try:
            user = CustomUserModel._default_manager.get_by_natural_key(username)
            otp_session = request.session.get("otp")
            sent_code = otp_session.get("code")
            str_expire_time = otp_session.get("str_expire_time")
            expire_time = datetime.datetime.strptime(
                str_expire_time, "%Y-%m-%d %H:%M:%S"
            )
            if sent_code and otp_code == str(sent_code):
                if datetime.datetime.now() < expire_time:
                    user = get_object_or_404(
                        CustomUserModel, phone_number=request.session["phone_number"]
                    )
                    del request.session["otp"]
                    return user
                else:
                    messages.error(
                        request, "The otp code has expired, try again.", "danger"
                    )
                    return None
        except CustomUserModel.DoesNotExist:
            del request.session["otp"]
            return None

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
