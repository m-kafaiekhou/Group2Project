from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from .models import CafeItem, Category
from django.views.generic import ListView, DetailView
from coffeeshop.models import Footer


# Create your views here.


"""class MenuSearch(View):
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
        )"""


class MenuSearch(ListView):
    model = CafeItem
    template_name = "menus/search_result.html"
    context_object_name = "searched_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        cd = self.request.GET.get("search", "")
        if cd:
            queryset = queryset.filter(
                Q(name__icontains=cd) | Q(description__icontains=cd)
            )
        return queryset


"""class Menu(View):
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
        return response"""


class Menu(ListView):
    model = CafeItem
    template_name = "menus/menu.html"
    context_object_name = "cafeitem"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["footer"] = Footer.objects.get(footer_name="main")

        return context


"""class MenuDetail(View):
    def get(self, request, cafeitme_name):
        cafeitem = CafeItem.objects.get(name=cafeitme_name)
        return render(request, "menus/detail.html", {"cafeitem": cafeitem})"""


class MenuDetail(DetailView):
    model = CafeItem
    template_name = "menus/detail.html"
    context_object_name = "cafeitem"
    slug_field = "name"
    slug_url_kwarg = "cafeitme_name"


class autocomplete(View):
#     def get(request):
#         if "term" in request.GET:
#             Qs = CafeItem.objects.filter(name__icontains=request.Get.get("term"))
#             names = list()
#             for i in Qs:
#                 names.append(i.name)
#             return JsonResponse(names, safe=False)
#         return render(request, "menu.html")
    pass
