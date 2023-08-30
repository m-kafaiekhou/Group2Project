from django.test import TestCase
from django.db import IntegrityError

from coffeeshop.models import Review, Footer, HomePage, Page, Navbar, Dashboard
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


class HomePageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.homepage = HomePage.objects.create(homepage_name="test homepage")

    def test_create_homepage(self):
        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(self.homepage.homepage_name, "test homepage")

    def test_default_vlaues(self):
        self.assertEqual(self.homepage.webpage_title, "TEHRAN Coffee Shop")
        self.assertEqual(self.homepage.search_section_is_active, True)
        self.assertEqual(self.homepage.search_section_title, "SEARCH")
        self.assertEqual(self.homepage.search_section_description, "Search for Drinks")
        self.assertEqual(self.homepage.search_placeholder, "Search Here")
        self.assertEqual(self.homepage.about_us_section_is_active, True)
        self.assertEqual(self.homepage.about_us_section_title, "ABOUT US")
        self.assertEqual(
            self.homepage.about_us_section_description, "Serving Since 2023"
        )
        self.assertEqual(self.homepage.about_us_image, "home_images/about.png")
        self.assertEqual(self.homepage.left_about_us_title, "Our Story")
        self.assertEqual(self.homepage.left_about_us_button_text, "Learn More")
        self.assertEqual(self.homepage.right_about_us_title, "Our Vision")
        self.assertEqual(
            self.homepage.right_about_us_first_option, "Lorem ipsum dolor sit amet"
        )
        self.assertEqual(self.homepage.our_services_section_is_active, True)
        self.assertEqual(self.homepage.our_services_section_title, "OUR SERVICES")
        self.assertEqual(
            self.homepage.our_services_section_description, "Fresh & Organic Beans"
        )
        self.assertEqual(self.homepage.offer_section_is_active, True)
        self.assertEqual(self.homepage.offer_section_title, "50% OFF")
        self.assertEqual(
            self.homepage.offer_section_short_description, "Sunday Special Offer"
        )
        self.assertEqual(
            self.homepage.offer_section_long_description,
            "Only for Sunday from 1st Jan to 30th Jan 2045",
        )
        self.assertEqual(self.homepage.menu_special_items_section_is_active, True)
        self.assertEqual(
            self.homepage.menu_special_items_section_title, "TOP RATED ITEMS"
        )
        self.assertEqual(
            self.homepage.menu_special_items_section_description,
            "The Best Items According to Our Customers",
        )
        self.assertEqual(self.homepage.testimonial_section_is_active, True)
        self.assertEqual(self.homepage.testimonial_section_title, "TESTIMONIAL")
        self.assertEqual(
            self.homepage.testimonial_section_description, "Our Clients Say"
        )

    def test_str_method(self):
        expected_str = "test homepage"
        self.assertEqual(str(self.homepage), expected_str)

    def test_unique_homepage_name(self):
        with self.assertRaises(IntegrityError):
            HomePage.objects.create(homepage_name="test homepage")


class PageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page = Page.objects.create(
            page_name="test page",
            webpage_title="test title",
            headername="test header",
            nestname="test nest",
        )

    def test_create_page(self):
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(self.page.page_name, "test page")
        self.assertEqual(self.page.webpage_title, "test title")
        self.assertEqual(self.page.headername, "test header")
        self.assertEqual(self.page.nestname, "test nest")

    def test_str_method(self):
        expected_str = "test page"
        self.assertEqual(str(self.page), expected_str)


class NavbarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.navbar = Navbar.objects.create(
            navbar_name="test navbar",
            cafe_name="test cafe",
        )

    def test_create_navbar(self):
        self.assertEqual(Navbar.objects.count(), 1)
        self.assertEqual(self.navbar.navbar_name, "test navbar")
        self.assertEqual(self.navbar.cafe_name, "test cafe")

    def test_str_method(self):
        expected_str = "test navbar"
        self.assertEqual(str(self.navbar), expected_str)

