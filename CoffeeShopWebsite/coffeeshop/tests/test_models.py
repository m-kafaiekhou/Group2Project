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
    @classmethod
    def setUpTestData(cls):
        cls.footer = Footer.objects.create(footer_name="test footer")

    def test_create_footer(self):
        self.assertEqual(Footer.objects.count(), 1)
        self.assertEqual(self.footer.footer_name, "test footer")

    def test_default_vlaues(self):
        self.assertEqual(self.footer.footer_is_active, True)
        self.assertEqual(self.footer.contact_us_title, "GET IN TOUCH")
        self.assertEqual(self.footer.address, "123 Street, New York, USA")
        self.assertEqual(self.footer.phone_number, "0211234567")
        self.assertEqual(self.footer.email, "info@example.com")
        self.assertEqual(self.footer.contact_us_is_active, True)
        self.assertEqual(self.footer.follow_us_title, "FOLLOW US")
        self.assertEqual(self.footer.twitter_link, "#")
        self.assertEqual(self.footer.facebook_link, "#")
        self.assertEqual(self.footer.linkedin_link, "#")
        self.assertEqual(self.footer.instagram_link, "#")
        self.assertEqual(self.footer.follow_us_is_active, True)
        self.assertEqual(self.footer.open_hours_title, "OPEN HOURS")
        self.assertEqual(self.footer.days1, "Monday- Friday")
        self.assertEqual(self.footer.hours1, "8:00 AM- 10:00 PM")
        self.assertEqual(self.footer.days2, "Saturday- Sunday")
        self.assertEqual(self.footer.hours2, "2:00 PM- 10:00 PM")
        self.assertEqual(self.footer.open_hours_is_active, True)
        self.assertEqual(self.footer.newsletter_title, "NEWSLETTER")
        self.assertEqual(
            self.footer.newsletter_description,
            "Enter your email to get the latest news",
        )
        self.assertEqual(self.footer.newsletter_is_active, True)

    def test_str_method(self):
        expected_str = "test footer"
        self.assertEqual(str(self.footer), expected_str)

    def test_unique_footer_name(self):
        with self.assertRaises(IntegrityError):
            Footer.objects.create(footer_name="test footer")
