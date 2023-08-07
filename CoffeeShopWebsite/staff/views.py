# from django.contrib.auth.views import LoginView
# from .forms import CustomAuthenticationForm
from django.shortcuts import render
from django.views import View
from .forms import CustomUserLoginForm

#
# class CustomLoginView(LoginView):
#     form_class = CustomAuthenticationForm


class CustomUserLoginView(View):
    form_class = CustomUserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, "staff/login.html", {"form": form})
