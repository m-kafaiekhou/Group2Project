from django.shortcuts import render
from .models import Order

# Create your views here.


def add_to_cart(response, item_pk: int, quantity: int) -> None:
    """
    sets a cookie to add items to shopping cart.

    item_pk and quantity turn into a list of dictionaries which is the
    value of the cart cookie.
    value = [{menu_item:quantity}, ...]
    """
    value = list()
    value.append({item_pk: quantity})

    str_value = str(value)
    max_age = 7 * 24 * 60 * 60
    response.set_cookie("cart", str_value, max_age=max_age)
