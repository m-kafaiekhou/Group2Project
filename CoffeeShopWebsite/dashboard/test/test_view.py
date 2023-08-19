from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from coffeeshop.models import Footer
from menus.models import Category, CafeItem
from staff.models import CustomUserModel
from orders.models import Order, OrderItem

class DashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.footer = Footer.objects.create()
        cls.staff = CustomUserModel.objects.create(
            phone_number='09030384898',
            first_name='testfname',
            last_name='testlname',
            password='Test123@',
            is_staff=True,
            is_active=True
        )

        cls.category = Category.objects.create(name='test')

        

    def test_url_exits_at_correct_location_for_dashboard_list_view(self):
        response1 = self.client.get("add-category/")
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get("add-item/")
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.get("category-list/")
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get("item-list/")
        self.assertEqual(response4.status_code, 200)
        response5 = self.client.get("order-list/")
        self.assertEqual(response5.status_code, 200)
        response6 = self.client.get("")
        self.assertEqual(response6.status_code, 200)


    def test_url_exits_at_correct_location_for_dashboard_detail_view(self):
        response7 = self.client.get("order-details/1/")
        self.assertEqual(response7.status_code, 200)
        response8 = self.client.get("order-details/1/quantity/")
        self.assertEqual(response8.status_code, 200)
        response9 = self.client.get("category-details/1/")
        self.assertEqual(response9.status_code, 200)
        response10 = self.client.get("item-details/1/")
        self.assertEqual(response10.status_code, 200)
        response11 = self.client.get("order-list/1/")
        self.assertEqual(response11.status_code, 200)

    def test_url_exits_at_correct_location_for_chart_list_view(self):
        response12 = self.client.get("chart/year-filter-options/")
        self.assertEqual(response12.status_code, 200)
        response13 = self.client.get("chart/month-filter-options/")
        self.assertEqual(response13.status_code, 200)
        response14 = self.client.get("chart/day-filter-options/")
        self.assertEqual(response14.status_code, 200)
        response15 = self.client.get("chart/sales/this-year/")
        self.assertEqual(response15.status_code, 200)
        response16 = self.client.get("chart/sales/this-month/")
        self.assertEqual(response16.status_code, 200)
        response17 = self.client.get("chart/sales/this-day/")
        self.assertEqual(response17.status_code, 200)
        response18 = self.client.get("chart/sales/daily-sum/")
        self.assertEqual(response18.status_code, 200)
        response19 = self.client.get("chart/sales/all-time/")
        self.assertEqual(response19.status_code, 200)
        response20 = self.client.get("chart/sales/best-customers/")
        self.assertEqual(response20.status_code, 200)
        response21 = self.client.get("chart/sales/category-sale/")
        self.assertEqual(response21.status_code, 200)
        response22 = self.client.get("chart/sales/employee-sales/")
        self.assertEqual(response22.status_code, 200)
        response23 = self.client.get("chart/sales/peak-hour/")
        self.assertEqual(response23.status_code, 200)
        response24 = self.client.get("chart/sales/popular-items/")
        self.assertEqual(response24.status_code, 200)


    def test_url_exits_at_correct_location_for_chart_detail_view(self):
        response25 = self.client.get("chart/sales/top-selling/year/")
        self.assertEqual(response25.status_code, 200)
        response26 = self.client.get("chart/sales/status/C/")
        self.assertEqual(response26.status_code, 200)