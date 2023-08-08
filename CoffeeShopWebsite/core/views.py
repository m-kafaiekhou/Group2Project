from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect


def error_404_view(request, exception):
    return render(request, "404.html")


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
                request.session["otp_code"] = code
                messages.success(
                    request, "کد تایید به شماره موبایل شما ارسال می شود", "success"
                )
                # print("#" * 100)
                # print(request.session["otp_code"])
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

            else:
                messages.error(request, "کد تایید نامعتبر است.", "danger")
                return redirect("verify_code")
