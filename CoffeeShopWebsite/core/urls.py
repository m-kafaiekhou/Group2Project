from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", include("pages.urls")),
    # path("phone/", views.PhoneNumberEntryView.as_view(), name="phone_entry"),
    path("code/", views.VerificationCodeEntryView.as_view(), name="code_entry"),
]

# handler404 = "pages.views.error_404_view"
admin.site.index_title = 'Group2 CoffeeShop'
admin.site.site_header = 'CoffeeShop Admin'
admin.site.site_title = 'CoffeeShop Admin'
