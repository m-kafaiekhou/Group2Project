from django.test import TestCase
from menus.models import Category, CafeItem
from coffeeshop.models import Footer
from orders.views import get_cart
from django.urls import reverse
from http.cookies import SimpleCookie
import tempfile
import json


class ViewsOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.footer = Footer.objects.create()
        cls.category = Category.objects.create(name='test')
        cls.cafeitem1 = CafeItem.objects.create(
            name='test1',
            description='test1',
            is_available=True,
            price=50,
            category=cls.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        cls.cafeitem2 = CafeItem.objects.create(
            name='test2',
            description='test2',
            is_available=True,
            price=10,
            category=cls.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        cls.cart = json.dumps({f'{cls.cafeitem1.id}': 1, f'{cls.cafeitem2.id}': 2})

    def test_cart_view(self):
        self.client.cookies = SimpleCookie({'cart': self.cart})
        response = self.client.get(reverse("orders:cart"))
        cart, total = get_cart(response.wsgi_request)
        expected = {self.cafeitem1: 1, self.cafeitem2: 2}
        self.assertEqual(cart, expected)
        self.assertEqual(total, 70)
        self.assertContains(response, self.cafeitem1.name)
        self.assertContains(response, self.cafeitem2.name)




