from django.test import TestCase
from menus.models import CafeItem, Category

class CafeItemTestClass(TestCase) :
    @classmethod
    def setUpTestData(cls) -> None:
        # return super().setUpTestData()
        CafeItem.objects.create(name='Espresso', description='Single')
    
    def setUp(self) -> None:
        return super().setUp()
    
    
