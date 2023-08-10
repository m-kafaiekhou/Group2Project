from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomAuthenticationForm
from staff.backends import CustomUserBackend
from core.utils import set_otp


class LoginUserView(View):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = CustomAuthenticationForm(request.POST)
        try:
            if form.is_valid():
                print("**************************************")
                print(form.cleaned_data)
                CUB = CustomUserBackend()
                user = CUB.authenticate(request, phone_number=form.cleaned_data["phone_number"],
                                                      password=form.cleaned_data["password"])
                print("********after")
                if user:
                    print("**************************************")
                    set_otp(request, user.phone_number)
                    return redirect("code_entry")
            else:
                messages.error(request, "Wrong Credentials!!")
                return render(request, self.template_name, context={'form': form})
        except:
            messages.error(request, "Please enter email and password for login!")
            return redirect('login')
