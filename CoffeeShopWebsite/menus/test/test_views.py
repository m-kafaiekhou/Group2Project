from django.test import TestCase
from django.urls import reverse
from views import Menu, MenuDetail, MenuSearch
from models import Category, CafeItem


class MenuViewTest(TestCase):
    
    def setUp(self) -> None:
        self.category = Category.objects.create(
            parent_category = 'Parent Test',
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
    def test_Menu_view(self):
        resp = self.client.get(self.menu_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/menu.html')

    def test_MenuDeatail_view(self):
        resp = self.client.get(self.menu_detail_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'menus/detail.html')