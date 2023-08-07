from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from core.utils import update_cart, create_session, delete_cart
from orders.models import Order, OrderItem
from menus.models import CafeItem

class CartView(View) :
    def post(request) :
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
                    request, "orders/cart.html", context={"items": cart, "total": total}
                )
            else:
                return redirect("menu")


class GetCart(View) :
    def get(request) :
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
                "orders/checkout.html",
                context={"items": cart, "total": total},
            )
        else:
            return redirect("menu")


def delete_cart_view(request):
    response = redirect("cart")
    delete_cart(request, response)
    return response
