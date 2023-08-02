from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name='cart'),
    path("checkout/", views.checkout_view, name='checkout'),
    path("menu/", views.menu, name="menu"),
    path("menu/search", views.menu_search, name='menu_search'),
    path("", views.home_page, name="home"),
]
