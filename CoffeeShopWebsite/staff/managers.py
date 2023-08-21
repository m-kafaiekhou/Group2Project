from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_active', True)

        if not phone_number:
            raise ValueError('You must provide an Phone number')

        user = self.model(phone_number=phone_number, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(phone_number, first_name, last_name, password, **other_fields)
