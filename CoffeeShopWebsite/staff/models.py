from django.db import models
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    _REGEX = r'09(\d{9})$'
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")

    phone_number = models.CharField('phone number', max_length=16, validators=[phone_validator], unique=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number
