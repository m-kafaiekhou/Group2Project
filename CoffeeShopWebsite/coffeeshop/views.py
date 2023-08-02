from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem, Order, OrderItem, Review, ParentCategory, SubCategory
from .search import SearchMenu


# Create your views here.


# First version for cookies and sessions without testing them.
# ----------------------------------------------------------------------------------------------------------------------
def add_to_cart(request, response, item_pk: int, quantity: int) -> None:
    """
    sets a cookie to add items to shopping cart.

    item_pk and quantity turn into a list of dictionaries which is the
    value of the cart cookie.
    value = [{menu_item:quantity}, ...]
    """
    if not request.COOKIES.get("cart"):
        value = list()
        value.append({item_pk: quantity})

        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)
    else:
        item_dict = {item_pk: quantity}
        v = request.COOKIES.get("cart")
        value = eval(v)
        value.append(item_dict)
        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)


def remove_from_cart(request, response, item_pk: int) -> None:
    """
    remove an item from the shopping cart, completely.
    """
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for dic in value:
            value.remove(dic[item_pk])
        delete_cart(request, response)

        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
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

        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)


def delete_cart(request, response) -> None:
    if request.COOKIES.get("cart"):
        response.delete_cookie("cart")


def create_session(request, order_id: int, phone_number: int) -> None:
    request.session["last_order_id"] = order_id
    request.session["phone_number"] = phone_number


def access_session(request):
    """
    checks if the session exists and then returnes a context containing
    order_history and last_order.

    if it does not exist an empty context will be returned.
    """
    if "last_order_id" and "phone_number" in request.session:
        order_id = request.session.get("last_order_id")
        last_order = Order.objects.get(pk=order_id)

        phone_number = request.session.get("phone_number")
        orders = Order.objects.filter(phone_number=phone_number)

        context = {"order_history": orders, "last_order": last_order}
        return render(request, "", context)
    else:
        context = {}
        return render(request, "", context)


# ----------------------------------------------------------------------------------------------------------------------


def home_page(request):
    top_rated_items = CafeItem.top_rated_items()
    return render(request, "coffeeshop/home.html", {"top_rated_items": top_rated_items})


def menu(request):
    cafeitem = CafeItem.objects.all()
    form = SearchMenu()
    if "search" in request.GET:
        form = SearchMenu(request.GET)
        if form.is_valid():
            cd = form.cleaned_data["search"]
            cafeitem = cafeitem.filter(
                Q(name__icontains=cd) | Q(description__icontains=cd)
            )
    return render(request, "menu/menu.html", {"cafeitem": cafeitem, "form": form})
