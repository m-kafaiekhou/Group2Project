from django.shortcuts import render
from django.views import View
# Create your views here.


class HomePage(View):

    def get(self, request, *args, **kwargs):
        # top_rated_items = CafeItem.top_rated_items()
        return render(request, "coffeeshop/home.html", {"top_rated_items": None})


class GalleryPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, "coffeeshop/gallery.html")