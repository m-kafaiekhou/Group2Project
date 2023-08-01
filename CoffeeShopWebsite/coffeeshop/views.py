from django.shortcuts import render, get_object_or_404, redirect
import json
from .models import CafeItem

# Create your views here.


def cart_view(request):
    request.COOKIES['cart'] = '[{"1":2}, {"2":3}]'
    cart = request.COOKIES.get('cart', None)
    if cart:
        items = json.loads(cart)
        object_lst = [CafeItem.objects.get(pk=pk) for item in items for pk in item.keys()]
        quantity_lst = [q for item in items for q in item.values()]
        items = {obj: quant for (obj, quant) in zip(object_lst, quantity_lst)}
        response = render(request, 'coffeeshop/cart.html', context={'items': items})
        response.set_cookie('cart', '[{"1":2}, {"2":3}]')

        return response
    else:
        return redirect('checkout')


def checkout_view(request):
    cart = request.COOKIES.get('cart', None)
    if cart:
        pass
    else:
        return redirect('login')
    return render(request, 'coffeeshop/checkout.html')
