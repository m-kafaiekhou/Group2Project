from django.urls import path
from . import views

urlpatterns = [
    path("cart/", cart_view, name='cart'),
    path("checkout/", checkout_view, name='checkout'),
    path("menu/", views.menu, name="menu"),
    path("", views.home_page, name="home"),
]
