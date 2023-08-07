from django.urls import path
from . import views


urlpatterns = [
    path("cart/", views.CartView.as_view(), name='cart'),
    path("checkout/", views.CheckoutView.as_view(), name='checkout'),
    path("delete-cart/", views.delete_cart_view, name='delete_cart'),
]
