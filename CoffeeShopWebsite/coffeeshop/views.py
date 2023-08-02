from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem, ParentCategory
from .search import SearchMenu


def hemo_page(request):
    top_rated_items = []
    return render(request, "coffeeshop/home.html", {"top_rated_items": top_rated_items})


def menu_search(request):
    cafeitem = CafeItem.objects.all()
    form = SearchMenu()
    if "search" in request.GET:
        form = SearchMenu(request.GET)
        if form.is_valid():
            cd = form.cleaned_data["search"]
            cafeitem = cafeitem.filter(
                Q(name__icontains=cd) | Q(description__icontains=cd)
            )
    return render(request, "menu/menu.html", {"cafeitem": cafeitem, "form": form}) #"coffeshop/menu_search.html"

def menu(request):
    cafeitem = CafeItem.objects.all()
    categories = ParentCategory.objects.all()
    return render(request, "coffeeshop/menu.html", {'cafeitem':cafeitem, 'categories': categories})