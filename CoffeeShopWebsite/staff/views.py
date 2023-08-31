from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login
from .forms import PhoneNumberForm, OtpForm
from staff.backends import CustomUserBackend
from core.utils import set_otp
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class LoginUserView(View):
    template_name = "registration/login.html"
    form1 = PhoneNumberForm
    form2 = OtpForm

    def get(self, request, *args, **kwargs):
        context = {
            "form1": self.form1,
            "form2": self.form2,
            "page_name": "login",
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if "form1_submit" in request.POST:
            phone_form = self.form1(request.POST)
            if phone_form.is_valid():
                phone_number = phone_form.cleaned_data["phone_number"]
                set_otp(request, phone_number)
            context = {"form1": phone_form, "form2": self.form2, "page_name": "login"}
            return render(request, self.template_name, context=context)

        if "form2_submit" in request.POST:
            otp_form = self.form2(request.POST)
            phone_number = request.session.get("phone_number")
            if otp_form.is_valid():
                otp_code = otp_form.cleaned_data["registration_code"]
                user = CustomUserBackend.authenticate(
                    self, request, phone_number=phone_number, otp_code=otp_code
                )
                if user:
                    login(request, user, backend="staff.backends.CustomUserBackend")
                    messages.success(request, "You logged in successfully!", "success")
                    return redirect("coffeeshop:home")
                messages.error(
                    request, "Phone number or registration code is wrong!", "warning"
                )
            context = {"form1": self.form1, "form2": otp_form}
            return render(request, self.template_name, context=context)


"""class LoginUserView(FormView):
    template_name = "registration/login.html"
    form_class1 = PhoneNumberForm
    form_class2 = OtpForm
    success_url = reverse_lazy('home')
    #context_form_name = 'form1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form1"] = self.get_form(self.form_class1)
        context["form2"] = self.get_form(self.form_class2)
        return context

    def form_valid(self, form):
        if "form1_submit" in self.request.POST:
            phone_number = form.cleaned_data["phone_number"]
            set_otp(self.request, phone_number)
            self.success_url = '/login/'
        elif "form2_submit" in self.request.POST:
            print("hello")
            otp_code = form.cleaned_data["registration_code"]
            phone_number = self.request.session.get("phone_number")
            user = CustomUserBackend.authenticate(self.request, phone_number=phone_number, otp_code=otp_code)
            if user:
                login(self.request, user, backend='staff.backends.CustomUserBackend')
                messages.success(self.request, "You logged in successfully!", "success")
                return super().form_valid(form)
            messages.error(self.request, "Phone number or registration code is wrong!", "warning")
        return self.render_to_response(self.get_context_data(form=form))"""

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
