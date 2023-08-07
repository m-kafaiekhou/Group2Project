from django.shortcuts import render
from django.views import View

# Create your views here.


class HomePage(View) :
    def get(request) :
        return render(request, "coffeeshop/home.html", {"top_rated_items": None})
