from django.test import TestCase
from menus.models import CafeItem, Category

class CafeItemTestClass(TestCase) :
    @classmethod
    def setUpTestData(cls) -> None:
        # return super().setUpTestData()
        CafeItem.objects.create(name='Espresso', description='Single')
    
    def test_name_label(self) :
        cafeitem = CafeItem.objects.get(id=1)
        field_label = cafeitem._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def setUp(self) -> None:
        return super().setUp()
    
    
