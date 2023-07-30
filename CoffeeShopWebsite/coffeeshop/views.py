from django.shortcuts import render
from django.views import generic

# Create your views here.

# class CartView(generic.DetailView):
def cart_view(request):
    return render(request, 'coffeeshop/cart.html')
