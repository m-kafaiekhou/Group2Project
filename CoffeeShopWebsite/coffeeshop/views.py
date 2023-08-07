from django.shortcuts import render
from django.views import View

# Create your views here.


def home_page(request):
    # top_rated_items = CafeItem.top_rated_items()
    return render(request, "coffeeshop/home.html", {"top_rated_items": None})
