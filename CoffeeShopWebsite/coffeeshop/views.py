from django.shortcuts import render, get_object_or_404, redirect
import json
from .models import CafeItem

# Create your views here.


def cart_view(request):
    request.COOKIES['cart'] = '[{"1":2}, {"2":3}]'
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

    return None


def checkout_view(request):
    cart, total = get_cart(request)
    if cart:
        return render(request, 'coffeeshop/checkout.html', context={'items': cart, 'total': total})
    else:
        return redirect('login')
