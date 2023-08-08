from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages
from .forms import PhoneNumberEntryForm, VerificationCodeEntryForm
from .utils import send_otp_code
import random


def error_404_view(request, exception):
    return render(request, "404.html")


class PhoneNumberEntryView(View):
    form_class = PhoneNumberEntryForm

    def get(self, request):
        form = self.form_class
        return render(request, "core/phone_entry.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            random_code = random.randint(1000, 9999)
            send_otp_code(phone_number=phone_number, code=random_code)
            request.session["otp_code"] = random_code
            messages.success(
                request, "کد تایید به شماره موبایل شما ارسال شد", "success"
            )
            return redirect("code_entry")

        return render(request, "core/phone_entry.html", {"form": form})


class VerificationCodeEntryView(View):
    form_class = VerificationCodeEntryForm

    def get(self, request):
        form = self.form_class
        return render(request, "core/code_entry.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data["verification_code"]
            if input_code == request.session["otp_code"]:
                del request.session["otp_code"]
                return redirect("home")

            else:
                messages.error(request, "کد تایید نامعتبر است.", "danger")
                return redirect("code_entry")
        return render(request, "core/code_entry.html", {"form": form})
