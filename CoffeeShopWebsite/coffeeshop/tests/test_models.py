from django.test import TestCase
from coffeeshop.models import Review, Footer
from menus.models import CafeItem, Category
class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="test category")
        cls.cafeitem = CafeItem.objects.create(
            name="test",
            description="for test",
            is_available=True,
            price=10,
            category=cls.category,
        )
        cls.review = Review.objects.create(
            rating=Review.Rating.VERY_HIGH,
            review="This is test review",
            cafeitem=cls.cafeitem,
        )
