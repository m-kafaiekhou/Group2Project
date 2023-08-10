from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages
from .forms import PhoneNumberEntryForm, VerificationCodeEntryForm
from django.contrib.auth import login
from staff.models import CustomUserModel


def error_404_view(request, exception):
    return render(request, "404.html", status=404)


class VerificationCodeEntryView(View):
    form_class = VerificationCodeEntryForm

    def get(self, request):
        form = self.form_class
        return render(request, "core/code_entry.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data["verification_code"]
            sent_code = request.session.get("otp_code")
            if sent_code and input_code == sent_code:
                user = get_object_or_404(CustomUserModel, phone_number=request.session['phone_number'])
                del request.session["otp_code"]
                login(request, user)
                return redirect("home")
            else:
                del request.session["otp_code"]
                messages.error(request, "کد تایید نامعتبر است.", "danger")
                return redirect("phone_entry")
        return render(request, "core/code_entry.html", {"form": form})
