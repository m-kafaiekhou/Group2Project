from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from core.utils import update_cart, create_session, delete_cart
from orders.models import Order, OrderItem
from menus.models import CafeItem
from django.views import View


class CartView(View):
    template_name = "orders/cart.html"
    fail_redirect_url = 'menu'

    def get(self, request, *args, **kwargs):
        cart, total = get_cart(request)
        if cart:
            return render(
                request, self.template_name, context={"items": cart, "total": total}
            )

        return redirect(self.fail_redirect_url)


def get_cart(request):
    cart = request.COOKIES.get("cart", None)
    if cart:
        items = eval(cart)
        pk_lst = []
        quantity_lst = []

        for pk, quant in items.items():
            pk_lst.append(pk)
            quantity_lst.append(quant)
        object_lst = get_list_or_404(CafeItem, id__in=pk_lst)

        items = {}
        total = 0
        for obj, quant in zip(object_lst, quantity_lst):
            items[obj] = quant
            total += obj.price * int(quant)
        return items, total

    return None, None


class CheckoutView(View):
    template_name = "orders/checkout.html"
    success_redirect_url = 'home'
    fail_redirect_url = 'menu'

    def get(self, request, *args, **kwargs):
        cart, total = get_cart(request)
        if cart:
            return render(
                request,
                self.template_name,
                context={"items": cart, "total": total},
            )
        else:
            return redirect(self.fail_redirect_url)

    def post(self, request, *args, **kwargs):
        cart, total = get_cart(request)
        phone_number = request.POST.get("phone_number")
        table_number = request.POST.get("table_number")
        order = Order.objects.create(
            phone_number=phone_number,
            table_number=table_number,
            total_price=total,
            status="d",
        )

        order_items = [
            OrderItem(order=order, cafeitem_id=item, quantity=quant)
            for item, quant in cart.items()
        ]

        OrderItem.objects.bulk_create(order_items)
        return redirect(self.success_redirect_url)


def delete_cart_view(request):
    response = redirect("cart")
    delete_cart(request, response)
    return response
