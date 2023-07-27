from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password, **other_fields):
        if not phone_number:
            raise ValueError('You must provide an Phone number')

        user = self.model(phone_number=phone_number, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()

        return user
