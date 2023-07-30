from django.shortcuts import render

# Create your views here.


def cart_view(request):
    return render(request, 'coffeeshop/cart.html')


def checkout_view(request):
    return render(request, 'coffeeshop/checkout.html')
