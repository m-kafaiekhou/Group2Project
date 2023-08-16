from django.db import models
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    _REGEX = r'09(\d{9})$'
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")

    phone_number = models.CharField(
        'phone number', max_length=14, validators=[phone_validator],
        unique=True, null=False
    )
    last_name = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now(),
                                      editable=False,
                                      blank=True, )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number
