from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # path("", include("pages.urls")),
    # path("phone/", views.PhoneNumberEntryView.as_view(), name="phone_entry"),
    # path("code/", views.VerificationCodeEntryView.as_view(), name="code_entry"),
]

# handler404 = "pages.views.error_404_view"
