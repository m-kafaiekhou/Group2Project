from django.test import TestCase
from orders.models import Order, OrderItem
from staff.models import CustomUserModel
from menus.models import CafeItem, Category
from datetime import datetime


class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = CustomUserModel.objects.create(
            phone_number='09036138552',
            first_name='testfirstname',
            last_name='testlastname',
            password='Test123@',
            is_staff=True,
            is_active=True
        )
        cls.order = Order.objects.create(
            status='D',
            staff=cls.staff,
            phone_number='09036138552',
            table_number=1,
        )

        cls.category = Category.objects.create(name='test')

        cls.cafeitem1 = CafeItem.objects.create(
            name='test1',
            description='test1',
            is_available=True,
            price=50,
            category=cls.category
        )
        cls.orderitem1 = OrderItem.objects.create(
            order=cls.order,
            cafeitem=cls.cafeitem1,
            quantity=2,
        ).set_price()

        cls.cafeitem2 = CafeItem.objects.create(
            name='test2',
            description='test2',
            is_available=True,
            price=10,
            category=cls.category
        )
        cls.orderitem2 = OrderItem.objects.create(
            order=cls.order,
            cafeitem=cls.cafeitem2,
            quantity=3,
        ).set_price()

    def setUp(self):
        pass

    """ Order Model Tests """

    def test_str_method_order(self):
        self.assertEqual(str(self.order), '09036138552')  # Test for phone number field happens here

    def test_fields_order(self):
        self.assertIsInstance(self.order.order_date, datetime)
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(self.order.status, 'D')
        self.assertEqual(self.order.staff, self.staff)

    """ OrderItem Model Tests"""

    def test_fields_orderitem(self):
        self.assertEqual(self.orderitem1.order, self.order)
        self.assertEqual(self.orderitem1.cafeitem, self.cafeitem1)
        self.assertEqual(self.orderitem1.quantity, 2)

    def test_set_price_orderitem(self):
        self.assertEqual(self.orderitem1.price, 100)

    """ Method Tests """

    def test_get_order_items_order(self):
        self.assertIn(self.orderitem1, self.order.get_order_items())
        self.assertIn(self.orderitem2, self.order.get_order_items())

    def test_get_total_price_order(self):
        self.assertEqual(self.order.get_total_price(), 130)
