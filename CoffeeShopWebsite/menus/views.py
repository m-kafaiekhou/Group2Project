from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem, Category
from core.utils import add_to_cart

# Create your views here.


def menu_search(request):
    if "search" in request.GET:
        cafeitem = CafeItem.objects.all()
        cd = request.GET.get("search")
        cafeitem = cafeitem.filter(Q(name__icontains=cd) | Q(description__icontains=cd))
        category = {obj.sub_category_fk.parent_category_fk for obj in cafeitem}

        return render(
            request,
            "coffeeshop/menu.html",
            {"cafeitem": cafeitem, "categories": category},
        )


def menu(request):
    item_pk = request.GET.get("pk", None)
    check = None
    if item_pk:
        check = 1
    cafeitem = CafeItem.objects.all()
    categories = Category.objects.all()
    response = render(
        request,
        "menus/menu.html",
        {"cafeitem": cafeitem, "categories": categories},
    )

    if check:
        response = add_to_cart(request, response, item_pk)
    return response
