from django.test import SimpleTestCase
from django.urls import reverse, resolve
from menus.views import MenuDetail, MenuSearch, Menu, autocomplete
from menus.models import Category, CafeItem


class UrlsTestClass(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            name='Cat Test',
        )

        cls.cafeitem = CafeItem.objects.create(
            name='Test',
            description='Just testing...',
            is_available=True,
            price=50,
            category=cls.category,
        )

    def test_menu(self):
        url = reverse("menus:menu")
        self.assertEquals(resolve(url).func.view_class, Menu)

    def test_menu_details(self):
        url = reverse("menus:menu_detail", kwargs={'cafeitem_name': self.cafeitem.slug()})
        self.assertEquals(resolve(url).func.view_class, MenuDetail)
