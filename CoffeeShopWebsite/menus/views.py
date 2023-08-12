from django.shortcuts import render
from django.db.models import Q
from django.views import View
from .models import CafeItem, Category


# Create your views here.


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        if "search" in request.GET:
            cd = request.GET.get("search")
            if cd != "":
                searched_items = CafeItem.objects.filter(
                    Q(name__icontains=cd) | Q(description__icontains=cd)
                )
            else: 
                return render(request, "menus/search_result.html", {"searched_items": None})
        return render(
            request,
            "menus/search_result.html",
            {"searched_items": searched_items},
        )


class Menu(View):
    def get(self, request, *args, **kwargs):
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


class MenuDetail(View):
    def get(self, request, cafeitme_name):
        cafeitem = CafeItem.objects.get(name=cafeitme_name)
        return render(request, "menus/detail.html", {"cafeitem": cafeitem})
