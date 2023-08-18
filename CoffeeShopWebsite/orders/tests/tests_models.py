from django.test import TestCase
from CoffeeShopWebsite.orders.models import Order
from CoffeeShopWebsite.staff.models import CustomUserModel


class OrderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = CustomUserModel.objects.create(
            phone_number = '09036138552',
            first_name = 'testfirstname',
            last_name = 'testlastname',
            password = 'Test123@',
            is_staff = True,
            is_active = True
        )

    def setUp(self):


    def test_status(self):
        pass

    def test_phone_number(self):
        pass

    def test_order_date(self):
        pass

    def test_table_number(self):
        pass

    def test_staff(self):
        pass

    def test_get_order_items(self):
        pass

    def test_get_total_price(self):
        pass
