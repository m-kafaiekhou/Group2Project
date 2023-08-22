from django.test import SimpleTestCase
from django.urls import reverse, resolve
from menus.views import MenuDetail, MenuSearch, Menu, autocomplete


class UrlsTestClass(SimpleTestCase):
    def test_menu(self):
        url = reverse("menus:menu")
        self.assertEquals(resolve(url).func.view_class, Menu)

    def test_menu_details(self):
        url = reverse("menus:detail", kwargs={'id': 1})
        self.assertEquals(resolve(url).func.view_class, MenuDetail)
