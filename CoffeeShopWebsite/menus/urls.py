from django.urls import path
from . import views


urlpatterns = [
    path(" ", views.autocomplete, name="autocomplete"),
    path("menu/", views.Menu.as_view(), name="menu"),
    path("menu/search/", views.MenuSearch.as_view(), name="menu_search"),
    # path("menu/detail/<str:cafeitme_name>", views.MenuDetail.as_view(), name="menu_detail"),
]
