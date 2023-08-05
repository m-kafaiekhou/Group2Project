from django.urls import path

urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("menu/search/", views.menu_search, name='menu_search'),
]
