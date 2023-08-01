from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem
from .search import SearchMenu
from .models import Order

# Create your views here.

def hemo_page(request):
    top_rated_items = []
    return render(request, "coffeeshop/home.html", {"top_rated_items": top_rated_items})

# First version for cookies and sessions without testing them.
# ----------------------------------------------------------------------------------------------------------------------
def add_to_cart(response, item_pk: int, quantity: int) -> None:
    """
    sets a cookie to add items to shopping cart.

    item_pk and quantity turn into a list of dictionaries which is the
    value of the cart cookie.
    value = [{menu_item:quantity}, ...]
    """
    value = list()
    str_pk = str(item_pk)
    str_q = str(quantity)
    value.append({str_pk: str_q})

    str_value = f"{value}"
    max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
    response.set_cookie("cart", str_value, max_age=max_age)


def remove_from_cart(request, response, item_pk: int) -> None:
    """
    remove an item from the shopping cart, completely.
    """
    str_pk = str(item_pk)
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for dic in value:
            value.remove(dic[str_pk])
        delete_cart(request, response)

        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)


def update_cart(request, response, item_pk: int, quantity: int) -> None:
    """
    updates the quantity of each item in the shopping cart.
    """
    str_pk = str(item_pk)
    str_q = str(quantity)
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for dic in value:
            if dic[str_pk]:
                value.update({str_pk: str_q})
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
