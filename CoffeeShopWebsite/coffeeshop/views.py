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


def remove_from_cart(request, response, item_pk: int) -> None:
    """
    remove an item from the shopping cart.
    """
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for dic in value:
            value.remove(dic[item_pk])
        delete_cart(request, response)

        str_value = str(value)
        max_age = 7 * 24 * 60 * 60
        response.set_cookie("cart", str_value, max_age=max_age)


def update_cart(request, response, item_pk: int, quantity: int) -> None:
    """
    updates the quantity of each item in the shopping cart.
    """
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for dic in value:
            if dic[item_pk]:
                value.update({item_pk: quantity})
        delete_cart(request, response)

        str_value = str(value)
        max_age = 7 * 24 * 60 * 60
        response.set_cookie("cart", str_value, max_age=max_age)
