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
        
