# from django.contrib.auth.views import LoginView
# from .forms import CustomAuthenticationForm
from django.shortcuts import render
from django.views import View
from .forms import CustomUserLoginForm
from core.utils import send_otp_code
import random

#
# class CustomLoginView(LoginView):
#     form_class = CustomAuthenticationForm


class CustomUserLoginView(View):
    form_class = CustomUserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, "staff/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
