from django.test import TestCase
from menus.models import Category, CafeItem
from orders.views import get_cart
from django.urls import reverse
from http.cookies import SimpleCookie
from orders.models import OrderItem, Order
import tempfile
import json


class ViewsOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="test")
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

    def test_cartempty_view(self):
        self.client.cookies = SimpleCookie({'cart': ''})
        response = self.client.get(reverse("orders:cart"))
        cart, total = get_cart(response.wsgi_request)
        self.assertEqual(cart, None)
        self.assertEqual(total, None)
        self.assertEqual(response.context['show_modal'], True)

    def test_checkout_get(self):
        self.client.cookies = SimpleCookie({'cart': self.cart})
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '70')

    def test_checkoutempty_get(self):
        self.client.cookies = SimpleCookie({'cart': ''})
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 302)

    def test_checkout_post(self):
        self.client.cookies = SimpleCookie({'cart': self.cart})
        data = {
            'phone_number': '09377584728',
            'table_number': '2'
        }
        response = self.client.post(reverse("orders:checkout"), data)
        orderitems = OrderItem.objects.all()
        self.assertEqual(orderitems[0].cafeitem, self.cafeitem1)
        self.assertEqual(orderitems[1].cafeitem, self.cafeitem2)
        order = Order.objects.all().last()
        self.assertEqual(order.get_total_price(), 70)

    def test_delete_cart(self):
        self.client.cookies = SimpleCookie({'cart': self.cart})
        response = self.client.get(reverse('orders:delete_cart'))
        self.assertEqual(response.status_code, 302)
        cart_after = self.client.cookies['cart'].value
        self.assertEqual(cart_after, '')






