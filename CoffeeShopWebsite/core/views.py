from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from .forms import PhoneNumberEntryForm, VerificationCodeEntryForm
from staff.models import CustomUserModel
import datetime


def error_404_view(request, exception):
    return render(request, "404.html", status=404)


class VerificationCodeEntryView(View):
    form_class = VerificationCodeEntryForm

    def get(self, request):
        form = self.form_class
        return render(request, "core/code_entry.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        otp_session = request.session.get("otp")
        if form.is_valid():
            input_code = form.cleaned_data["verification_code"]
            sent_code = otp_session.get("code")
            str_expire_time = otp_session.get("str_expire_time")
            expire_time = datetime.datetime.strptime(
                str_expire_time, "%Y-%m-%d %H:%M:%S"
            )
            if sent_code and input_code == sent_code:
                if datetime.datetime.now() < expire_time:
                    user = get_object_or_404(
                        CustomUserModel, phone_number=request.session["phone_number"]
                    )
                    del request.session["otp"]
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(
                        request, "The otp code has expired, try again.", "danger"
                    )
                    return redirect("phone_entry")
            else:
                del request.session["otp"]
                messages.error(request, "The otp code is wrong, try again.", "danger")
                return redirect("phone_entry")
        return render(request, "core/code_entry.html", {"form": form})
