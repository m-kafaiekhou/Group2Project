from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from core.utils import create_session, delete_cart
from orders.models import Order, OrderItem
from menus.models import CafeItem
from django.views import View


class CartView(View):
    template_name = "orders/cart.html"

    def get(self, request, *args, **kwargs):
        cart, total = get_cart(request)
        context = {"items": cart, "total": total}
        if not cart:
            context["show_modal"] = True
        return render(request, self.template_name, context=context)


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
    success_redirect_url = "delete_cart"
    fail_redirect_url = "menu"

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
            status="D",
        )

        order_items = [
            OrderItem(order=order, cafeitem=item, quantity=quant).set_price()
            for item, quant in cart.items()
            if item is not None
        ]

        OrderItem.objects.bulk_create(order_items)

        return redirect(self.success_redirect_url)


class DeleteCartView(View):
    success_redirect_url = "home"

    def get(self, request, *args, **kwargs):
        response = redirect(self.success_redirect_url)
        delete_cart(request, response)
        return response

class OrderHistoryView(View) :
    template_name = 'order_history.html'
    model_class = Order
    form_class = None
    def get(self, request, *args, **kwargs) :
        last_order_id = request.session.get('last_order_id')
        
        if last_order_id :
            
            last_order = request.session.get('last_order_id')
            
            if last_order.status == 'A' :
                orders = self.model_class.objects.filter(phone_number = request.session.get('phone_number'))
            
            else :
                orders = last_order
        
        return render(request, self.template_name, context= {"orders" : orders})


    def post(self,request, *args, **kwargs) :
        pass