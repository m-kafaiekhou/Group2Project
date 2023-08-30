# from .forms import PhoneNumberEntryForm, VerificationCodeEntryForm
from staff.models import CustomUserModel
import datetime
from django.views.generic import TemplateView
from django.shortcuts import render


def error_404_view(request, exception):
    return render(request, "404.html", status=404)


# this generic class based view is for 404 Error handling. please use this view instead of error_404_view(request, exception)
# in the main urls.py: we put -> handler404 = NotFoundView.get_rendered_view()
class NotFoundView(TemplateView):
    template_name = "errors/404.html"

    @classmethod
    def get_rendered_view(cls):
        as_view_fn = cls.as_view()

        def view_fn(request):
            response = as_view_fn(request)
            # this is what was missing before
            response.render()
            return response

        return view_fn
