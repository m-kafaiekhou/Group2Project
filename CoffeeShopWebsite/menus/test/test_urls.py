from django.test import SimpleTestCase
from django.urls import reverse,resolve
from menus.views import MenuDetail, MenuSearch, Menu, autocomplete

class UrlsTestClass(SimpleTestCase):
        
    def test_menu(self):
        url=reverse("menus:menu")
        self.assertEquals(resolve(url).func.view_class,Menu)