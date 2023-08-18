from django.test import TestCase
from orders.models import Order
from staff.models import CustomUserModel
from datetime import datetime


class OrderTestCase(TestCase):
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

    def setUp(self):
        self.order = Order.objects.create(
            status='D',
            staff=self.staff,
            table_number=1,
        )

    def test_str_method(self):
        self.assertEqual(str(self.order, '09036138552'))  # Test for phone number field happens here

    def test_fields(self):
        self.assertIsInstance(self.order.order_date, datetime)
        self.assertEqual(self.order.staff, self.staff)

    def test_staff(self):
        pass

    def test_get_order_items(self):
        pass

    def test_get_total_price(self):
        pass
