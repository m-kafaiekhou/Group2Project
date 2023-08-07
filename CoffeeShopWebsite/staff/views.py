# from django.contrib.auth.views import LoginView
# from .forms import CustomAuthenticationForm
from django.views import View
from .forms import CustomUserLoginForm

#
# class CustomLoginView(LoginView):
#     form_class = CustomAuthenticationForm


class CustomUserLoginView(View):
    pass
