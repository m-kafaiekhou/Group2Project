from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import CafeItem, Order, OrderItem, Review, ParentCategory, SubCategory
from .search import SearchMenu
import json

# Create your views here.


# First version for cookies and sessions without testing them.
# ----------------------------------------------------------------------------------------------------------------------
def add_to_cart(request, response, item_pk: int) -> None:
    """
    sets a cookie to add items to shopping cart.

    item_pk and quantity turn into a list of dictionaries which is the
    value of the cart cookie.
    value = [{menu_item:quantity}, ...]
    """
    cart = request.COOKIES.get("cart", None)
    if not cart:
        value = list()
        value.append({item_pk: 1})
        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)
    else:
        cart = json.loads(cart)
        for dic in cart:
            for key, val in dic.items():
                if key == item_pk:
                    old_val = val
        item_dict = {item_pk: old_val+1}
        cart.append(item_dict)
        str_value = f"{cart}"
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
    # top_rated_items = CafeItem.top_rated_items()
    return render(request, "coffeeshop/home.html", {"top_rated_items": None})


def menu_search(request):
    cafeitem = CafeItem.objects.all()
    form = SearchMenu()
    if "search" in request.GET:
        form = SearchMenu(request.GET)
        if form.is_valid():
            cd = form.cleaned_data["search"]
            cafeitem = cafeitem.filter(
                Q(name__icontains=cd) | Q(description__icontains=cd)
            )
    return render(request, "menu/menu.html", {"cafeitem": cafeitem, "form": form}) #"coffeshop/menu_search.html"


def cart_view(request):
    cart, total = get_cart(request)
    if cart:
        return render(request, 'coffeeshop/cart.html', context={'items': cart, 'total': total})
    else:
        return redirect('checkout')


def get_cart(request):
    cart = request.COOKIES.get('cart', None)
    if cart:
        items = json.loads(cart)
        object_lst = [CafeItem.objects.get(pk=pk) for item in items for pk in item.keys()]
        quantity_lst = [q for item in items for q in item.values()]
        items = {}
        total = 0
        for obj, quant in zip(object_lst, quantity_lst):
            items[obj] = quant
            total += obj.price * quant
        return items, total

    return None, None


def checkout_view(request):
    cart, total = get_cart(request)
    if cart:
        return render(request, 'coffeeshop/checkout.html', context={'items': cart, 'total': total})
    else:
        return redirect('login')


def menu(request):
    item_pk = request.GET.get('pk', None)
    check = None
    if item_pk:
        check = 1
    cafeitem = CafeItem.objects.all()
    categories = ParentCategory.objects.all()
    response = render(request, "coffeeshop/menu.html", {'cafeitem':cafeitem, 'categories': categories})

    if check:
        add_to_cart(request, response, item_pk)
    return response
