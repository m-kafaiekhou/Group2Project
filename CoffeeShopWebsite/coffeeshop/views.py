from django.shortcuts import render

# Create your views here.


def add_to_cart(response, value: list[dict(str, int)]) -> None:
    """
    This function sets a cookie and follows cart behavior.

    value is a list of dictionaries:
    [{menu_item:quantity}, ...]
    """
    max_age = 7 * 24 * 60 * 60
    response.set_cookie("cart", value, max_age=max_age)
