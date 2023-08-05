from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem, Order, OrderItem, Review, Category

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
        )  # "coffeshop/menu_search.html"




def menu(request):
    item_pk = request.GET.get("pk", None)
    check = None
    if item_pk:
        check = 1
    cafeitem = CafeItem.objects.all()
    categories = Category.objects.all()
    response = render(
        request,
        "coffeeshop/menu.html",
        {"cafeitem": cafeitem, "categories": categories},
    )

    if check:
        response = add_to_cart(request, response, item_pk)
    return response


class CafeItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="cafe_item/", blank=True, null=True)
    is_available = models.BooleanField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
    )

    @property
    def item_rate(self):
        reviews = self.review_set
        rates = [rev.rating for rev in reviews]
        return sum(rates) / len(rates)

    @classmethod
    def top_rated_items(cls):
        return CafeItem.objects.annotate(item_rate=Avg("review_set__rating")).order_by(
            "-item_rate"
        )[:3]

    def category_name(self):
        return self.category.parent_category

    def __str__(self) -> str:
        return self.name