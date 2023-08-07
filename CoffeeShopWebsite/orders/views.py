from django.shortcuts import render, get_object_or_404, redirect
from core.utils import update_cart, create_session, delete_cart
from orders.models import Order, OrderItem
from menus.models import CafeItem
from django.views import View


class CartView(View):
    template_name = "orders/cart.html"

    def get(self, request, *args, **kwargs):
        cart, total = get_cart(request)
        if cart:
            return render(
                request, self.template_name, context={"items": cart, "total": total}
            )

        return redirect("menu")


def get_cart(request):
    cart = request.COOKIES.get("cart", None)
    if cart:
        items = eval(cart)
        object_lst = [get_object_or_404(CafeItem, pk=int(pk)) for pk, _ in items.items()]
        quantity_lst = [quant for _, quant in items.items()]
        items = {}
        total = 0
        for obj, quant in zip(object_lst, quantity_lst):
            items[obj] = quant
            total += obj.price * int(quant)
        return items, total

    return None, None


class CheckoutView(View):
    template_name = "orders/checkout.html"

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.cart, self.total = get_cart(request=self.request)

    def get(self, request, *args, **kwargs):
        if self.cart:
            return render(
                request,
                self.template_name,
                context={"items": self.cart, "total": self.total},
            )
        else:
            return redirect("menu")

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get("phone_number")
        table_number = request.POST.get("table_number")
        order = Order.objects.create(
            phone_number=phone_number,
            table_number=table_number,
            total_price=self.total,
            status="d",
        )
        object_lst = [obj for obj, _ in self.cart.items()]
        quantity_lst = [val for _, val in self.cart.items()]
        zipped = zip(object_lst, quantity_lst)
        for item, quant in zipped:
            OrderItem.objects.create(order_fk=order, cafeitem_fk=item, quantity=quant)

        create_session(request, phone_number=phone_number, order_id=order.id)
        return redirect("home")

# def checkout_view(request):
#     cart, total = get_cart(request)
#     if request.method == "POST":
#         phone_number = request.POST.get("phone_number")
#         table_number = request.POST.get("table_number")
#         order = Order.objects.create(
#             phone_number=phone_number,
#             table_number=table_number,
#             total_price=total,
#             status="d",
#         )
#         object_lst = [obj for obj, _ in cart.items()]
#         quantity_lst = [val for _, val in cart.items()]
#         zipped = zip(object_lst, quantity_lst)
#         for item, quant in zipped:
#             OrderItem.objects.create(order_fk=order, cafeitem_fk=item, quantity=quant)
#
#         create_session(request, phone_number=phone_number, order_id=order.id)
#         return redirect("home")
#
#     else:
#         if cart:
#             return render(
#                 request,
#                 "orders/checkout.html",
#                 context={"items": cart, "total": total},
#             )
#         else:
#             return redirect("menu")


def delete_cart_view(request):
    response = redirect("cart")
    delete_cart(request, response)
    return response
