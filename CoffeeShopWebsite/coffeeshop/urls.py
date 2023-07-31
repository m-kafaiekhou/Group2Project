from django.urls import path
from . import views

urlpatterns = [path("home/", views.hemo_page, name="home")]
