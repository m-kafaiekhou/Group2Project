from django.urls import path
from . import views

app_name = "menus"
urlpatterns = [
    path("auto/", views.autocomplete.as_view(), name="autocomplete"),
    path("", views.Menu.as_view(), name="menu"),
    path("search/", views.MenuSearch.as_view(), name="menu_search"),
    # path("menu/detail/<str:cafeitme_name>", views.MenuDetail.as_view(), name="menu_detail"),
]
