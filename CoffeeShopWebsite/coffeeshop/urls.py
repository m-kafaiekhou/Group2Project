from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("menu/search", views.menu_search, name='menu_search'),
    path("home/", views.hemo_page, name="home"),
]
