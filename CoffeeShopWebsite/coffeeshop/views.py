from django.shortcuts import render
from .models import Order

# Create your views here.


# First version for cookies and sessions without testing them.
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


def delete_cart(request, response) -> None:
    if request.COOKIES.get("cart"):
        response.delete_cookie("cart")


def create_session(request, order_id: int, phone_number: int) -> None:
    request.session["last_order_id"] = order_id
    request.session["phone_number"] = phone_number


def access_session(request):
    if "last_order_id" in request.session:
        order_id = request.session.get("last_order_id")
        last_order = Order.objects.get(pk=order_id)
        context = {"last_order": last_order}
        return render(request, "", context)

    if "phone_number" in request.session:
        phone_number = request.session.get("phone_number")
        orders = Order.objects.filter(phone_number=phone_number)
        context = {"order_history": orders}
        return render(request, "", context)
