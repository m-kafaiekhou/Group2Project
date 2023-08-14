from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import PhoneNumberForm, OtpForm
from staff.backends import CustomUserBackend
from core.utils import set_otp


class LoginUserView(View):
    template_name = "registration/login.html"
    form1 = PhoneNumberForm
    form2 = OtpForm
    context = {"form1": form1, "form2": form2}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        if "form1_submit" in request.POST:
            phone_form = self.from1(request.POST)
            if phone_form.is_valid():
                phone_number = phone_form.cleaned_data["phone_number"]
                set_otp(request, phone_number)
            return render(request, self.template_name, context=self.context)

        if "form2_submit" in request.POST:
            otp_form = self.form2(request.POST)
            if otp_form.is_valid():
                otp_code = otp_form.cleaned_data["registration_code"]
                user = CustomUserBackend.authenticate(
                    phone_number=phone_number, otp_code=otp_code
                )
                if user:
                    login(request, user)
                    messages.success(request, "You logged in successfully!", "success")
                    return redirect("home")
            return render(request, self.template_name, context=self.context)

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     form = CustomAuthenticationForm(request.POST)
    #     try:
    #         if form.is_valid():
    #             CUB = CustomUserBackend()
    #             user = CUB.authenticate(
    #                 request,
    #                 phone_number=form.cleaned_data["phone_number"],
    #                 password=form.cleaned_data["password"],
    #             )
    #             if user:
    #                 set_otp(request, user.phone_number)
    #                 return redirect("code_entry")
    #         else:
    #             messages.error(request, "Wrong Credentials!!")
    #             return render(request, self.template_name, context={"form": form})
    #     except:
    #         messages.error(request, "Please enter email and password for login!")
    #         return redirect("login")
