from django.urls import path
from . import views


urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("menu/search/", views.MenuSearch.as_view(), name='menu_search'),
]
