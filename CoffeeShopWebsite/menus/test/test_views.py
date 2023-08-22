from django.test import TestCase
from django.urls import reverse
# from menus.views import Menu, MenuDetail, MenuSearch
from menus.models import Category, CafeItem


class MenuViewTest(TestCase):
    
    def setUp(self) -> None:
        self.parCategory = Category.objects.create(
            name='Par Cat Test',
        )
        self.category = Category.objects.create(
            parent_category = self.parCategory,
            name = 'Cat Test',
        )
        
        self.cafeitem = CafeItem.objects.create(
            name='Test', 
            description='Just testing...',
            is_available=True,
            price=50,
            category=self.category,
        )
        
        self.menu_url = reverse("menus:menu")
        self.menu_detail_url = reverse("menus:detail")
        self.menu_search_url = reverse("menus:search_result")

    def test_Menu_view(self):
        resp = self.client.get(self.menu_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/menu.html')

    def test_MenuDeatail_view(self):
        resp = self.client.get(self.menu_detail_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/detail.html')

    def test_MenuSearch_view(self):
        resp = self.client.get(self.menu_search_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/search_result.html')

    def test_search_view(self):
        resp = self.client.get(self.search_url,{'search':'esp'})
        self.assertEqual(CafeItem.objects.filter(title__contains='esp').count(),1)
        self.assertEqual(CafeItem.objects.filter(title__contains='kljhgfcb').count(),0)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/search_result.html')