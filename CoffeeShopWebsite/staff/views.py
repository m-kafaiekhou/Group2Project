# from django.contrib.auth.views import LoginView
# from .forms import CustomAuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import CustomUserLoginForm, VerifyCodeForm
from .models import CustomUserModel
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
        phone_number = form.cleaned_data["phone_number"]
        if form.is_valid():
            if CustomUserModel.objects.filter(phone_number=phone_number).exists():
                code = random.randint(1000, 9999)
                send_otp_code(phone_number=form.cleaned_data["phone_number"], code=code)
                request.session["otp_code"] = {phone_number: code}
                messages.success(
                    request, "کد تایید به شماره موبایل شما ارسال می شود", "success"
                )
                return redirect("verify_code")
        return redirect("login")


class CustomUserLoginVerifyView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "staff/verify.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data["verify_code"]
            if input_code == request.session["otp_code"]:
                pass

            del request.session["otp_code"]
