import tempfile
import datetime
from PIL import Image
from menus.models import CafeItem, Category
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import slugify
from coffeeshop.models import Review
from django.urls import reverse


class CafeItemTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(name="Test Category")
        cls.cafeitem = CafeItem.objects.create(
            name='Test',
            description='Just testing...',
            is_available=True,
            price=50,
            category=cls.category,
        )
        cls.review1 = Review.objects.create(review='test', cafeitem=cls.cafeitem)
        cls.review2 = Review.objects.create(rating=5, review='test', cafeitem=cls.cafeitem)


    def test_create_cafeitem(self):
        self.assertEqual(self.cafeitem.name, "Test")
        self.assertEqual(self.cafeitem.description, 'Just testing...')
        self.assertEqual(self.cafeitem.is_available, True)
        self.assertEqual(self.cafeitem.price, 50)
        self.assertEqual(self.cafeitem.category, self.category)
        self.assertIsInstance(self.cafeitem.date_added, datetime.datetime)

    def test_name_label(self):
        cafeitem = CafeItem.objects.get(id=1)
        field_label = cafeitem._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_max_length(self):
        cafeitem = CafeItem.objects.get(id=1)
        max_length = cafeitem._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)

    def test_name_max_length(self):
        cafeitem = CafeItem.objects.get(id=1)
        max_length = cafeitem._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_str_method(self):
        expected_str = "Test"
        self.assertEqual(str(self.cafeitem.name), expected_str)

    def test_slug_method(self):
        expected_slug = "test"
        self.assertEqual(self.cafeitem.slug(), expected_slug)

    def test_get_absolute_url(self):
        exc = reverse("menus:menu_detail", kwargs={"pk": self.cafeitem.pk})
        self.assertEqual(self.cafeitem.get_absolute_url(), exc)

    def test_item_rate(self):
        exc = 4.5
        self.assertEqual(self.cafeitem.item_rate, exc)

    def test_category_name(self):
        self.assertEqual(self.cafeitem.category_name(), None)


class CategoryTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parCategory = Category.objects.create(
            name='Par Cat Test',
        )
        cls.category = Category.objects.create(
            parent_category=cls.parCategory,
            name='Cat Test',
        )
        cls.cafeitem = CafeItem.objects.create(
            name='Test',
            description='Just testing...',
            is_available=True,
            price=50,
            category=cls.category,
        )

    def test_create_category(self):
        self.assertEqual(self.category.name, "Cat Test")
        self.assertEqual(self.category.parent_category, self.parCategory)
        self.assertIsInstance(self.cafeitem.date_added, datetime.datetime)

    def test_str_method(self):
        expected_str = "Cat Test"
        self.assertEqual(str(self.category), expected_str)
