from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("delete-cart/", views.DeleteCartView.as_view(), name="delete_cart"),
    path("order-history/", views.OrderHistoryView.as_view(), name="order_history"),
]
