from django.shortcuts import render
from django.db.models import Q
from django.views import View
from .models import CafeItem, Category
from core.utils import add_to_cart


# Create your views here.

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        if "search" in request.GET:
            cafeitem = CafeItem.objects.all()
            cd = request.GET.get("search")
            cafeitem = cafeitem.filter(Q(name__icontains=cd) | Q(description__icontains=cd))
            category = {obj.sub_category_fk.parent_category_fk for obj in cafeitem}
        return render(
            request,
            "menus/menu.html",
            {"cafeitem": cafeitem, "categories": category},
        )


class Menu(View) :
    def get(self, request, *args, **kwargs) :
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
    def get(self, request, cafeitem_name):
        cafeitme = CafeItem.objects.get(name=cafeitem_name)