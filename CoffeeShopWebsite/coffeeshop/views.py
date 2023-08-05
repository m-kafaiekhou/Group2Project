from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import CafeItem, Order, OrderItem, Review, Category
from .forms import SearchMenu
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
        value.append({f"{item_pk}": 1})
        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)
    else:
        cart = eval(cart)
        old_val = 0
        # print(cart, "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
        for i in range(len(cart)):
            print(i, "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
            for key, val in cart[i].items():
                # print(key, val, cart[i], "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
                if key == item_pk:
                    old_val = val
                    cart.pop(i)
            if old_val == val:
                break
        item_dict = {item_pk: old_val + 1}
        cart.append(item_dict)
        str_value = f"{cart}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)
    return response


def remove_from_cart(request, response, item_pk: int):
    """
    remove an item from the shopping cart, completely.
    """
    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        value = eval(v)
        for i in range(value):
            if value[i].key == item_pk:
                value.pop(i)
        delete_cart(request, response)

        str_value = f"{value}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)


def update_cart(request, response, item_pk: int, quantity: int):
    """
    updates the quantity of each item in the shopping cart.
    """

    if request.COOKIES.get("cart"):
        v = request.COOKIES.get("cart")
        cart = eval(v)
        for i in range(len(cart)):
            for key, val in cart[i].items():
                if int(key) == item_pk:
                    cart.append({f"{item_pk}": quantity})
                    cart.pop(i)
        delete_cart(request, response)

        str_value = f"{cart}"
        max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
        response.set_cookie("cart", str_value, max_age=max_age)
        return response


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
    if "search" in request.GET:
        cafeitem = CafeItem.objects.all()
        cd = request.GET.get("search")
        cafeitem = cafeitem.filter(Q(name__icontains=cd) | Q(description__icontains=cd))
        category = {obj.sub_category_fk.parent_category_fk for obj in cafeitem}

        return render(
            request,
            "coffeeshop/menu.html",
            {"cafeitem": cafeitem, "categories": category},
        )  # "coffeshop/menu_search.html"


def cart_view(request):
    cart, total = get_cart(request)
    if request.method == "POST":
        response = redirect("cart")
        for obj, val in cart.items():
            print(obj, val, "_*_*_*_*_*_")
            quantity = int(request.POST.get(f"{obj.id}"))
            response = update_cart(request, response, quantity=quantity, item_pk=obj.id)

        return response
    else:
        if cart:
            return render(
                request, "coffeeshop/cart.html", context={"items": cart, "total": total}
            )
        else:
            return redirect("menu")


def get_cart(request):
    cart = request.COOKIES.get("cart", None)
    if cart:
        items = eval(cart)
        object_lst = [get_object_or_404(CafeItem, pk=pk) for item in items for pk in item.keys()]
        quantity_lst = [q for item in items for q in item.values()]
        items = {}
        total = 0
        for obj, quant in zip(object_lst, quantity_lst):
            items[obj] = quant
            total += obj.price * int(quant)
        return items, total

    return None, None


def checkout_view(request):
    cart, total = get_cart(request)
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        table_number = request.POST.get("table_number")
        order = Order.objects.create(
            phone_number=phone_number,
            table_number=table_number,
            total_price=total,
            status="d",
        )
        object_lst = [obj for obj, _ in cart.items()]
        quantity_lst = [val for _, val in cart.items()]
        zipped = zip(object_lst, quantity_lst)
        for item, quant in zipped:
            OrderItem.objects.create(order_fk=order, cafeitem_fk=item, quantity=quant)

        create_session(request, phone_number=phone_number, order_id=order.id)
        return redirect("home")

    else:
        if cart:
            return render(
                request,
                "coffeeshop/checkout.html",
                context={"items": cart, "total": total},
            )
        else:
            return redirect("menu")


def menu(request):
    item_pk = request.GET.get("pk", None)
    check = None
    if item_pk:
        check = 1
    cafeitem = CafeItem.objects.all()
    categories = Category.objects.all()
    response = render(
        request,
        "coffeeshop/menu.html",
        {"cafeitem": cafeitem, "categories": categories},
    )

    if check:
        response = add_to_cart(request, response, item_pk)
    return response


def delete_cart_view(request):
    response = redirect("cart")
    delete_cart(request, response)
    return response
