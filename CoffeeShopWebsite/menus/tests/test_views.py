from django.test import TestCase
from django.urls import reverse

# from menus.views import Menu, MenuDetail, MenuSearch
from menus.models import Category, CafeItem
import tempfile


class MenuViewTest(TestCase):
    def setUp(self) -> None:
        self.parCategory = Category.objects.create(
            name="Par Cat Test",
        )
        self.category = Category.objects.create(
            parent_category=self.parCategory,
            name="Cat Test",
        )

        self.cafeitem = CafeItem.objects.create(
            name="Test",
            description="Just testing...",
            is_available=True,
            price=50,
            category=self.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        )

        self.menu_url = reverse("menus:menu")
        self.menu_detail_url = reverse(
            "menus:menu_detail", kwargs={"pk": self.cafeitem.pk}
        )
        self.menu_search_url = reverse("menus:menu_search")

    def test_Menu_view(self):
        resp = self.client.get(self.menu_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "menus/menu.html")

    def test_MenuDetail_view(self):
        print(
            "********************************",
            self.menu_detail_url,
            "*****************************************",
        )
        resp = self.client.get(self.menu_detail_url)
        print(resp)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "menus/detail.html")

    def test_MenuSearch_view(self):
        resp = self.client.get(self.menu_search_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "menus/search_result.html")

    def test_search_view(self):
        resp = self.client.get(self.menu_search_url, {"search": "esp"})
        self.assertEqual(CafeItem.objects.filter(name__contains="Tes").count(), 1)
        self.assertEqual(CafeItem.objects.filter(name__contains="kljhgfcb").count(), 0)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "menus/search_result.html")
