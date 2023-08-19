from django.test import TestCase
from coffeeshop.models import Review, Footer
from menus.models import CafeItem, Category
import datetime


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

    def test_create_review(self):
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.review.rating, Review.Rating.VERY_HIGH)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.review, "This is test review")
        self.assertEqual(self.review.cafeitem, self.cafeitem)
        self.assertIsInstance(self.review.date_added, datetime.datetime)

    def test_default_rating(self):
        review = Review.objects.create(
            review="test default rating",
            cafeitem=self.cafeitem,
        )

        self.assertEqual(review.rating, Review.Rating.HIGH)
        self.assertEqual(review.rating, 4)

    def test_str_method(self):
        expected_str = "This is test re ..."
        self.assertEqual(str(self.review), expected_str)


class FooterModelTest(TestCase):
