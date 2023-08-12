from django.db import models
from django.db.models import Avg
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category", blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    


class CafeItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="cafe_item/", blank=True, null=True)
    is_available = models.BooleanField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
    )
    
    def get_absolute_url(self) :
        return reverse("cafeitem_detail", kwargs={"slug": self.slug})

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
